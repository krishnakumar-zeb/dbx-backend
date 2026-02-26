"""
Presidio utility for PII detection and anonymization.
Supports country-specific PII entity detection using Presidio's built-in recognizers
plus programmatically registered custom recognizers for entities not in Presidio.

PERSON Entity Enhancement:
- Automatically includes titles (Mr, Mrs, Dr, etc.) before names
- Automatically expands to include last names (capitalized words after first name)
- Example: "Mr. John Khan" is detected as a single PERSON entity
"""
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from typing import List, Dict, Optional
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from utility.exceptions import PresidioException
from utility.country_pii_config import (
    get_entities_for_country,
    DEFAULT_COUNTRY,
)
from utility.custom_recognizers import get_custom_recognizers
import logging

logger = logging.getLogger(__name__)


class ConsistentAnonymizer:
    """
    Consistent anonymization with AES-CBC encryption.
    Same PII value always maps to the same tag (e.g. "Bob" -> <PERSON_0>).
    """

    __slots__ = ("crypto_key", "value_to_tag", "tag_to_encrypted",
                 "tag_to_metadata", "counters")

    def __init__(self, crypto_key: str):
        key_bytes = crypto_key.encode("utf-8")
        self.crypto_key = key_bytes.ljust(32, b"0")[:32]
        self.value_to_tag: Dict[str, str] = {}
        self.tag_to_encrypted: Dict[str, str] = {}
        self.tag_to_metadata: Dict[str, dict] = {}
        self.counters: Dict[str, int] = {}

    def encrypt_value(self, plaintext: str) -> str:
        """AES-CBC encrypt. Returns Base64(IV + ciphertext)."""
        try:
            iv = os.urandom(16)
            cipher = AES.new(self.crypto_key, AES.MODE_CBC, iv)
            ct = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
            return base64.b64encode(iv + ct).decode("utf-8")
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise PresidioException(f"Failed to encrypt value: {e}")

    def operator_logic(self, original_value: str, entity_type: str) -> str:
        """Return a consistent indexed tag for *original_value*."""
        existing = self.value_to_tag.get(original_value)
        if existing:
            return existing

        idx = self.counters.get(entity_type, 0)
        self.counters[entity_type] = idx + 1
        tag = f"<{entity_type}_{idx}>"

        self.value_to_tag[original_value] = tag
        self.tag_to_encrypted[tag] = self.encrypt_value(original_value)
        return tag

    def get_mapping_with_metadata(self, entities: List[RecognizerResult]) -> Dict:
        """Build {tag: {encrypted_value, entity_type, score}} mapping."""
        # Pre-build a lookup: entity_type -> best score
        best_scores: Dict[str, float] = {}
        for e in entities:
            cur = best_scores.get(e.entity_type, 0.0)
            if e.score > cur:
                best_scores[e.entity_type] = e.score

        return {
            tag: {
                "encrypted_value": enc_val,
                "entity_type": self._extract_entity_type_from_tag(tag),
                "score": best_scores.get(self._extract_entity_type_from_tag(tag), 0.0),
            }
            for tag, enc_val in self.tag_to_encrypted.items()
        }
    
    def _extract_entity_type_from_tag(self, tag: str) -> str:
        """
        Extract entity type from tag.
        Examples:
            <PERSON_0> -> PERSON
            <US_DRIVER_LICENSE_0> -> US_DRIVER_LICENSE
            <EMAIL_ADDRESS_1> -> EMAIL_ADDRESS
        """
        # Remove < and > brackets
        tag_content = tag.strip("<>")
        # Split by underscore and remove the last part (which is the counter)
        parts = tag_content.rsplit("_", 1)
        # Return everything except the counter
        return parts[0] if len(parts) > 1 else tag_content


class PresidioUtility:
    """Presidio PII detection & anonymization with country-specific support."""

    def __init__(self, chunk_size: int = 100000, nlp_engine_type: str = None):
        """
        Initialize Presidio utility.
        
        Args:
            chunk_size: Maximum characters per chunk (default: 100,000)
                       Chunks break at natural boundaries (newlines, periods)
                       No overlap needed with smart chunking
            nlp_engine_type: Type of NLP engine to use (default: from env var NLP_ENGINE_TYPE or "spacy")
                           Options: "spacy", "transformers", "spacy_small"
        """
        try:
            # Get NLP engine type from parameter or environment variable
            if nlp_engine_type is None:
                nlp_engine_type = os.getenv("NLP_ENGINE_TYPE", "spacy")
            
            # Initialize NLP engine
            from utility.nlp_config import get_nlp_engine, get_current_model_info
            nlp_engine = get_nlp_engine(nlp_engine_type)
            
            # Get model info for logging
            model_info = get_current_model_info(nlp_engine)
            logger.info(f"NLP Engine: {model_info['engine_type']}")
            for lang, info in model_info['models'].items():
                logger.info(f"  Language '{lang}': {info}")
            
            # Initialize Presidio with custom NLP engine
            self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
            self.anonymizer = AnonymizerEngine()
            
            # Register custom recognizers programmatically
            custom_recognizers = get_custom_recognizers()
            for recognizer in custom_recognizers:
                self.analyzer.registry.add_recognizer(recognizer)
            
            # Chunking configuration
            self.chunk_size = chunk_size
            
            logger.info("Presidio engines initialised")
            logger.info(f"Loaded {len(self.analyzer.registry.recognizers)} recognizers "
                       f"({len(custom_recognizers)} custom)")
            logger.info(f"Smart chunking enabled: chunk_size={chunk_size} (natural boundaries)")
        except Exception as e:
            raise PresidioException(f"Failed to initialise Presidio: {e}")

    # ------------------------------------------------------------------
    # Chunking Methods
    # ------------------------------------------------------------------
    def should_chunk(self, text: str) -> bool:
        """
        Check if text needs chunking based on configured chunk size.
        
        Args:
            text: Text to check
            
        Returns:
            True if text exceeds chunk_size and needs chunking
        """
        return len(text) > self.chunk_size
    
    def create_chunks(self, text: str) -> List[Dict]:
        """
        Split text into chunks at natural boundaries (newlines, periods).
        No overlap needed since we break at clean boundaries.
        
        Args:
            text: Text to split into chunks
            
        Returns:
            List of chunk dictionaries with text and offset information
        """
        chunks = []
        start = 0
        text_len = len(text)
        chunk_num = 0
        
        while start < text_len:
            chunk_num += 1
            
            # If remaining text is smaller than limit, take it all
            if text_len - start <= self.chunk_size:
                chunks.append({
                    'chunk_number': chunk_num,
                    'text': text[start:],
                    'start_offset': start,
                    'end_offset': text_len,
                    'length': text_len - start
                })
                break
            
            # Look for natural break point within chunk size
            end_search = start + self.chunk_size
            
            # Priority 1: Newline (paragraph break)
            break_point = text.rfind("\n", start, end_search)
            
            # Priority 2: Sentence end (period + space)
            # Only use if newline is in first 80% of chunk (prefer paragraph breaks)
            if break_point == -1 or break_point < (start + int(self.chunk_size * 0.8)):
                period_break = text.rfind(". ", start, end_search)
                if period_break != -1:
                    break_point = period_break + 1  # Include the period
            
            # If no clean break found in last 20% of chunk, force the limit
            if break_point == -1:
                break_point = end_search
            
            chunk_text = text[start:break_point].strip()
            
            chunks.append({
                'chunk_number': chunk_num,
                'text': chunk_text,
                'start_offset': start,
                'end_offset': break_point,
                'length': len(chunk_text)
            })
            
            start = break_point
        
        logger.info(f"Created {len(chunks)} chunks from {text_len:,} characters "
                   f"(avg: {text_len // len(chunks):,} chars/chunk)")
        return chunks
    
    def process_chunks(
        self,
        chunks: List[Dict],
        language: str = "en",
        country: str = DEFAULT_COUNTRY
    ) -> List[RecognizerResult]:
        """
        Process each chunk with Presidio and adjust entity positions.
        No deduplication needed since chunks don't overlap.
        
        Args:
            chunks: List of chunk dictionaries from create_chunks()
            language: Language code
            country: Country name for country-specific entities
            
        Returns:
            List of all entities with positions adjusted to original text
        """
        all_entities = []
        
        for chunk_info in chunks:
            chunk_num = chunk_info['chunk_number']
            chunk_text = chunk_info['text']
            start_offset = chunk_info['start_offset']
            
            # Get entity list for this country
            entities = get_entities_for_country(country)
            
            # Detect PII in this chunk
            chunk_entities = self.analyzer.analyze(
                text=chunk_text,
                language=language,
                entities=entities,
            )
            
            # Filter by score
            chunk_entities = [e for e in chunk_entities if e.score >= 0.4 and e.entity_type in entities]
            
            # Adjust entity positions to match original text
            for entity in chunk_entities:
                entity.start += start_offset
                entity.end += start_offset
            
            all_entities.extend(chunk_entities)
            
            logger.debug(f"Chunk {chunk_num} ({start_offset:,}-{chunk_info['end_offset']:,}): "
                        f"{len(chunk_entities)} entities")
        
        logger.info(f"Processed {len(chunks)} chunks, found {len(all_entities)} entities total")
        return all_entities
    


    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------
    def detect_pii(
        self,
        text: str,
        language: str = "en",
        country: str = DEFAULT_COUNTRY,
    ) -> List[RecognizerResult]:
        """
        Detect PII entities using country-specific rules.
        
        Automatically uses smart chunking for large documents. Chunks break
        at natural boundaries (newlines, periods) so no overlap or deduplication needed.
        
        Presidio automatically uses its built-in and custom recognizers based on
        the entity list provided. No manual recognizer registration needed.
        
        Args:
            text: Text to analyze
            language: Language code (default: "en")
            country: Country name for country-specific entities
            
        Returns:
            List of detected PII entities with scores >= 0.4
        """
        try:
            if not text or not text.strip():
                return []

            # Check if chunking is needed
            if self.should_chunk(text):
                logger.info(f"Text length ({len(text):,} chars) exceeds chunk size ({self.chunk_size:,}), using smart chunking")
                
                # Create chunks at natural boundaries
                chunks = self.create_chunks(text)
                
                # Process chunks (no deduplication needed with natural boundaries)
                all_entities = self.process_chunks(chunks, language, country)
                
                # Resolve overlapping entities
                resolved = self._resolve_overlapping_entities(all_entities)
                
                # Enhance PERSON detection with titles (Mr, Mrs, Ms, Dr, etc.)
                enhanced = self._enhance_person_with_titles(text, resolved)
                
                # Filter ETHNICITY false positives using context analysis
                context_filtered = self._filter_ethnicity_false_positives(text, enhanced)
                
                # Filter out our own anonymization tags
                filtered = self._filter_anonymization_tags(text, context_filtered)
                
                logger.info(f"Detected {len(filtered)} PII entities for country={country} (chunked)")
                return filtered
            else:
                # Text is small enough, process normally
                logger.debug(f"Text length ({len(text):,} chars) within chunk size, processing normally")
                
                # Get entity list for this country (9 common + 5 country-specific)
                entities = get_entities_for_country(country)

                # Presidio automatically uses the appropriate recognizers
                results = self.analyzer.analyze(
                    text=text,
                    language=language,
                    entities=entities,
                )

                # Filter by score and requested entities only
                filtered = [e for e in results if e.score >= 0.4 and e.entity_type in entities]
                resolved = self._resolve_overlapping_entities(filtered)
                
                # Enhance PERSON detection with titles (Mr, Mrs, Ms, Dr, etc.)
                enhanced = self._enhance_person_with_titles(text, resolved)
                
                # Filter ETHNICITY false positives using context analysis
                context_filtered = self._filter_ethnicity_false_positives(text, enhanced)
                
                # Filter out our own anonymization tags
                final = self._filter_anonymization_tags(text, context_filtered)
                
                logger.info(f"Detected {len(final)} PII entities for country={country}")
                return final
                
        except Exception as e:
            raise PresidioException(f"PII detection failed: {e}")

    # ------------------------------------------------------------------
    # Anonymization
    # ------------------------------------------------------------------
    def anonymize_text(
        self,
        text: str,
        entities: List[RecognizerResult],
    ) -> Dict:
        """Anonymize detected PII with consistent mapping + AES encryption."""
        try:
            if not entities:
                return {
                    "anonymized_text": text,
                    "mapping": {},
                    "encryption_key": "",
                    "entities_count": 0,
                }

            # CRITICAL: Resolve overlapping entities again before anonymization
            # This prevents the [E1010] spaCy error about overlapping spans
            entities = self._resolve_overlapping_entities(entities)
            
            if not entities:
                return {
                    "anonymized_text": text,
                    "mapping": {},
                    "encryption_key": "",
                    "entities_count": 0,
                }

            encryption_key = os.urandom(16).hex()
            mapper = ConsistentAnonymizer(crypto_key=encryption_key)

            entity_types = {e.entity_type for e in entities}
            operators = {
                et: OperatorConfig(
                    "custom",
                    {"lambda": lambda val, _et=et: mapper.operator_logic(val, _et)},
                )
                for et in entity_types
            }

            result = self.anonymizer.anonymize(
                text=text,
                analyzer_results=entities,
                operators=operators,
            )

            mapping = mapper.get_mapping_with_metadata(entities)
            logger.info(f"Anonymised {len(mapping)} unique PII values")

            return {
                "anonymized_text": result.text,
                "mapping": mapping,
                "encryption_key": encryption_key,
                "entities_count": len(entities),
            }
        except Exception as e:
            raise PresidioException(f"Anonymization failed: {e}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _resolve_overlapping_entities(
        entities: List[RecognizerResult],
    ) -> List[RecognizerResult]:
        """
        Resolve overlapping entities by prioritizing highest score.
        
        This method ensures NO overlapping entities remain, which prevents
        the spaCy [E1010] error during anonymization.
        
        Strategy:
        1. Sort by score (highest first)
        2. Keep entities that don't overlap with already selected ones
        3. Return sorted by position
        """
        if not entities:
            return []
        
        # Sort by score (highest first), then by start position
        sorted_by_score = sorted(entities, key=lambda x: (-x.score, x.start))
        
        resolved: List[RecognizerResult] = []
        
        for entity in sorted_by_score:
            # Check if this entity overlaps with any already resolved entity
            has_overlap = False
            for resolved_entity in resolved:
                # Check for ANY overlap
                if not (entity.end <= resolved_entity.start or entity.start >= resolved_entity.end):
                    has_overlap = True
                    break
            
            # Only add if no overlap
            if not has_overlap:
                resolved.append(entity)
        
        # Sort by start position for final output
        resolved.sort(key=lambda x: x.start)
        
        # Log if we removed overlapping entities
        removed_count = len(entities) - len(resolved)
        if removed_count > 0:
            logger.debug(f"Removed {removed_count} overlapping entities (kept highest scores)")
        
        return resolved
    
    @staticmethod
    def _filter_anonymization_tags(
        text: str,
        entities: List[RecognizerResult]
    ) -> List[RecognizerResult]:
        """
        Filter out entities that are actually our own anonymization tags.
        
        This prevents tags like <LOCATION_0> from being detected as PII
        and masked again (e.g., <LOCATION_0> -> <LOCATION_7>).
        
        Args:
            text: The text being analyzed
            entities: List of detected entities
            
        Returns:
            Filtered list without tag entities
        """
        import re
        
        # Pattern to match our anonymization tags: <ENTITY_TYPE_NUMBER>
        tag_pattern = re.compile(r'<[A-Z_]+_\d+>')
        
        filtered = []
        for entity in entities:
            # Extract the text for this entity
            entity_text = text[entity.start:entity.end]
            
            # Check if this entity is actually one of our tags
            if tag_pattern.fullmatch(entity_text):
                # This is our own tag, skip it
                logger.debug(f"Filtered out anonymization tag: {entity_text}")
                continue
            
            # Check if this entity is INSIDE a tag
            # Look at surrounding context to see if it's part of a tag
            context_start = max(0, entity.start - 1)
            context_end = min(len(text), entity.end + 1)
            context = text[context_start:context_end]
            
            # If surrounded by < and >, it's part of a tag
            if context.startswith('<') and context.endswith('>'):
                logger.debug(f"Filtered out text inside tag: {entity_text}")
                continue
            
            # This is a real entity, keep it
            filtered.append(entity)
        
        removed_count = len(entities) - len(filtered)
        if removed_count > 0:
            logger.info(f"Filtered out {removed_count} anonymization tags from detection")
        
        return filtered
    
    @staticmethod
    def _filter_ethnicity_false_positives(
        text: str,
        entities: List[RecognizerResult]
    ) -> List[RecognizerResult]:
        """
        Filter out ETHNICITY entities that are likely false positives based on context.
        
        Common false positives:
        - "American company" (nationality/origin, not ethnicity)
        - "Indian food" (cuisine, not ethnicity)
        - "White paper" (color, not ethnicity)
        - "Black Friday" (color, not ethnicity)
        - "German language" (language, not ethnicity)
        
        Keep ETHNICITY entities when:
        - Preceded by ethnicity-related keywords (race, ethnicity, identifies as, etc.)
        - In demographic/personal information context
        - Part of a list of ethnicities
        
        Args:
            text: The text being analyzed
            entities: List of detected entities
            
        Returns:
            Filtered list with ETHNICITY false positives removed
        """
        import re
        
        # Words that commonly appear with ambiguous ethnicity terms (false positive indicators)
        false_positive_indicators = [
            # Business/Organization
            r'\b(company|corporation|corp|business|firm|organization|org|enterprise|inc|llc)\b',
            # Food/Cuisine
            r'\b(food|cuisine|restaurant|dish|recipe|meal|cooking|kitchen)\b',
            # Language
            r'\b(language|speaking|speak|speaks|spoken|tongue|dialect)\b',
            # Geography/Location
            r'\b(country|nation|state|city|region|area|territory|border)\b',
            # Products/Goods
            r'\b(product|goods|item|merchandise|brand|style)\b',
            # Colors (for White/Black)
            r'\b(paper|color|colour|paint|shirt|dress|car|house|box|bag)\b',
            # Events
            r'\b(friday|monday|tuesday|wednesday|thursday|saturday|sunday|day|week|month)\b',
            # Nationality/Citizenship (not ethnicity)
            r'\b(citizen|citizenship|national|nationality|passport|visa)\b',
        ]
        
        # Combine into one pattern
        false_positive_pattern = re.compile(
            '|'.join(false_positive_indicators),
            re.IGNORECASE
        )
        
        # Keywords that indicate TRUE ethnicity context (keep these)
        true_ethnicity_indicators = [
            r'\b(race|racial|ethnicity|ethnic|heritage|ancestry|descent|origin|background)\b',
            r'\b(identifies as|identify as|self-identify|self-identified)\b',
            r'\b(demographic|demographics|diversity|multicultural|minority|majority)\b',
            r'\b(african american|asian american|native american|hispanic|latino|latina)\b',
        ]
        
        # Combine into one pattern
        true_ethnicity_pattern = re.compile(
            '|'.join(true_ethnicity_indicators),
            re.IGNORECASE
        )
        
        # Ambiguous terms that need context checking (common false positives)
        ambiguous_terms = {
            'american', 'indian', 'white', 'black', 'asian', 'european',
            'german', 'french', 'italian', 'spanish', 'chinese', 'japanese',
            'mexican', 'canadian', 'british', 'english', 'irish', 'scottish',
            'african', 'latin', 'arab', 'arabic', 'jewish', 'native'
        }
        
        filtered = []
        
        for entity in entities:
            # Only filter ETHNICITY entities
            if entity.entity_type != "ETHNICITY":
                filtered.append(entity)
                continue
            
            # Extract the entity text
            entity_text = text[entity.start:entity.end].lower().strip()
            
            # If it's not an ambiguous term, keep it (likely a specific ethnicity)
            if entity_text not in ambiguous_terms:
                filtered.append(entity)
                continue
            
            # For ambiguous terms, check context (50 chars before and after)
            context_start = max(0, entity.start - 50)
            context_end = min(len(text), entity.end + 50)
            context = text[context_start:context_end]
            
            # Check if context indicates TRUE ethnicity
            if true_ethnicity_pattern.search(context):
                # Strong indicator this is a real ethnicity reference
                filtered.append(entity)
                logger.debug(f"Kept ETHNICITY '{entity_text}' - true ethnicity context found")
                continue
            
            # Check if context indicates FALSE positive
            if false_positive_pattern.search(context):
                # Likely a false positive (e.g., "American company", "Indian food")
                logger.debug(f"Filtered ETHNICITY '{entity_text}' - false positive context: {context[max(0, entity.start - context_start - 20):min(len(context), entity.end - context_start + 20)]}")
                continue
            
            # No strong indicators either way
            # For ambiguous cases, use a conservative approach:
            # - Keep if score is very high (>0.8)
            # - Filter if score is moderate (<0.8)
            if entity.score >= 0.8:
                filtered.append(entity)
                logger.debug(f"Kept ETHNICITY '{entity_text}' - high confidence score: {entity.score:.2f}")
            else:
                logger.debug(f"Filtered ETHNICITY '{entity_text}' - ambiguous context, moderate score: {entity.score:.2f}")
        
        removed_count = len([e for e in entities if e.entity_type == "ETHNICITY"]) - len([e for e in filtered if e.entity_type == "ETHNICITY"])
        if removed_count > 0:
            logger.info(f"Filtered out {removed_count} ETHNICITY false positives using context analysis")
        
        return filtered
    
    @staticmethod
    def _enhance_person_with_titles(
        text: str,
        entities: List[RecognizerResult]
    ) -> List[RecognizerResult]:
        """
        Enhance PERSON detection by:
        1. Including titles (Mr, Mrs, Ms, Dr, etc.) before names
        2. Expanding to include adjacent capitalized words (last names)
        
        If a PERSON entity is detected:
        - Look backward for titles and include them
        - Look forward for capitalized words (likely last names) and include them
        
        Args:
            text: The text being analyzed
            entities: List of detected entities
            
        Returns:
            Enhanced list with expanded PERSON entities
        """
        import re
        
        # Common titles to detect (case-insensitive)
        titles = [
            r'\bMr\.?',      # Mr, Mr.
            r'\bMrs\.?',     # Mrs, Mrs.
            r'\bMs\.?',      # Ms, Ms.
            r'\bMiss\.?',    # Miss, Miss.
            r'\bDr\.?',      # Dr, Dr.
            r'\bProf\.?',    # Prof, Prof.
            r'\bSir\.?',     # Sir, Sir.
            r'\bMadam\.?',   # Madam, Madam.
            r'\bLady\.?',    # Lady, Lady.
            r'\bLord\.?',    # Lord, Lord.
            r'\bRev\.?',     # Rev, Rev.
            r'\bFr\.?',      # Fr, Fr. (Father)
            r'\bSr\.?',      # Sr, Sr. (Sister/Senior)
            r'\bJr\.?',      # Jr, Jr. (Junior)
            r'\bEsq\.?',     # Esq, Esq. (Esquire)
        ]
        
        # Combine all titles into one pattern
        title_pattern = re.compile(
            r'(' + '|'.join(titles) + r')\s+',
            re.IGNORECASE
        )
        
        # Pattern for capitalized words (potential last names)
        # Matches: Khan, Smith, O'Brien, McDonald, etc.
        capitalized_word_pattern = re.compile(
            r"^[A-Z][a-z]+(?:'[A-Z][a-z]+)?(?:\s+[A-Z][a-z]+)*"
        )
        
        enhanced = []
        
        for entity in entities:
            # Only enhance PERSON entities
            if entity.entity_type != "PERSON":
                enhanced.append(entity)
                continue
            
            new_start = entity.start
            new_end = entity.end
            
            # STEP 1: Check if there's a title before this person
            # Look back up to 10 characters before the entity
            lookback_start = max(0, entity.start - 10)
            prefix_text = text[lookback_start:entity.start]
            
            # Search for title at the end of prefix
            title_match = None
            for match in title_pattern.finditer(prefix_text):
                # Keep the last match (closest to the person name)
                title_match = match
            
            if title_match:
                # Calculate the actual position of the title in the original text
                new_start = lookback_start + title_match.start()
            
            # STEP 2: Check if there are capitalized words after this person (last names)
            # Look forward up to 50 characters after the entity
            lookahead_end = min(len(text), entity.end + 50)
            suffix_text = text[entity.end:lookahead_end]
            
            # Skip leading whitespace
            suffix_text_stripped = suffix_text.lstrip()
            whitespace_len = len(suffix_text) - len(suffix_text_stripped)
            
            # Check if next word(s) are capitalized
            cap_match = capitalized_word_pattern.match(suffix_text_stripped)
            if cap_match:
                # Found capitalized word(s) after the person name
                # Expand entity to include them
                new_end = entity.end + whitespace_len + cap_match.end()
            
            # Create expanded entity if we made any changes
            if new_start != entity.start or new_end != entity.end:
                from presidio_analyzer import RecognizerResult
                expanded_entity = RecognizerResult(
                    entity_type="PERSON",
                    start=new_start,
                    end=new_end,
                    score=entity.score
                )
                
                expanded_text = text[new_start:new_end]
                original_text = text[entity.start:entity.end]
                logger.debug(f"Enhanced PERSON: '{original_text}' → '{expanded_text}'")
                
                enhanced.append(expanded_entity)
            else:
                # No changes, keep original entity
                enhanced.append(entity)
        
        return enhanced


# ============================================================
# Module-level helpers (used by UnmaskService)
# ============================================================

def decrypt_value(encrypted_blob: str, crypto_key: str) -> str:
    """Decrypt a single AES-CBC encrypted value."""
    try:
        key_bytes = crypto_key.encode("utf-8").ljust(32, b"0")[:32]
        data = base64.b64decode(encrypted_blob)
        iv, ct = data[:16], data[16:]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode("utf-8")
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise PresidioException(f"Failed to decrypt value: {e}")


def deanonymize_text(
    anonymized_text: str, mapping: Dict, encryption_key: str
) -> str:
    """Replace tags with decrypted original values."""
    try:
        result = anonymized_text
        for tag, meta in mapping.items():
            decrypted = decrypt_value(meta["encrypted_value"], encryption_key)
            result = result.replace(tag, decrypted)
        return result
    except Exception as e:
        raise PresidioException(f"De-anonymization failed: {e}")
