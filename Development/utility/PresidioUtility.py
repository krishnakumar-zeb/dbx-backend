"""
Presidio utility for PII detection and anonymization.
Supports country-specific PII entity detection using Presidio's built-in recognizers
plus programmatically registered custom recognizers for entities not in Presidio.
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
                "entity_type": tag.split("_")[0].strip("<>"),
                "score": best_scores.get(tag.split("_")[0].strip("<>"), 0.0),
            }
            for tag, enc_val in self.tag_to_encrypted.items()
        }


class PresidioUtility:
    """Presidio PII detection & anonymization with country-specific support."""

    def __init__(self, chunk_size: int = 900000, chunk_overlap: int = 500):
        """
        Initialize Presidio utility.
        
        Args:
            chunk_size: Maximum characters per chunk (default: 90,000)
                       Set below spaCy limit to leave safety margin
            chunk_overlap: Characters to overlap between chunks (default: 500)
                          Ensures entities at boundaries are not missed
        """
        try:
            # Initialize Presidio with default recognizers
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            
            # Register custom recognizers programmatically
            custom_recognizers = get_custom_recognizers()
            for recognizer in custom_recognizers:
                self.analyzer.registry.add_recognizer(recognizer)
            
            # Chunking configuration
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
            
            logger.info("Presidio engines initialised")
            logger.info(f"Loaded {len(self.analyzer.registry.recognizers)} recognizers "
                       f"({len(custom_recognizers)} custom)")
            logger.info(f"Chunking enabled: chunk_size={chunk_size}, overlap={chunk_overlap}")
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
        Split text into overlapping chunks.
        
        Args:
            text: Text to split into chunks
            
        Returns:
            List of chunk dictionaries with text and offset information
        """
        chunks = []
        text_length = len(text)
        start = 0
        chunk_num = 0
        
        while start < text_length:
            chunk_num += 1
            end = min(start + self.chunk_size, text_length)
            
            chunk_info = {
                'chunk_number': chunk_num,
                'text': text[start:end],
                'start_offset': start,
                'end_offset': end,
                'length': end - start
            }
            
            chunks.append(chunk_info)
            
            # Move to next chunk with overlap
            if end >= text_length:
                break
            start = end - self.chunk_overlap
        
        logger.info(f"Created {len(chunks)} chunks from {text_length:,} characters")
        return chunks
    
    def process_chunks(
        self,
        chunks: List[Dict],
        language: str = "en",
        country: str = DEFAULT_COUNTRY
    ) -> List[RecognizerResult]:
        """
        Process each chunk with Presidio and adjust entity positions.
        
        Args:
            chunks: List of chunk dictionaries from create_chunks()
            language: Language code
            country: Country name for country-specific entities
            
        Returns:
            List of all entities with positions adjusted to original text
        """
        all_entities = []
        entities_by_chunk = []
        
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
            entities_by_chunk.append(len(chunk_entities))
            
            logger.debug(f"Chunk {chunk_num} ({start_offset:,}-{chunk_info['end_offset']:,}): "
                        f"{len(chunk_entities)} entities")
        
        logger.info(f"Processed {len(chunks)} chunks, found {len(all_entities)} entities total")
        return all_entities
    
    def deduplicate_entities(
        self,
        entities: List[RecognizerResult]
    ) -> List[RecognizerResult]:
        """
        Remove duplicate entities from overlapping regions.
        
        Two entities are duplicates if they have:
        - Same entity type
        - Similar positions (within 5 characters)
        
        Args:
            entities: List of entities (possibly with duplicates)
            
        Returns:
            Deduplicated list of entities
        """
        if not entities:
            return []
        
        # Sort by position and score (keep highest score for duplicates)
        sorted_entities = sorted(
            entities,
            key=lambda x: (x.start, x.end, -x.score)
        )
        
        deduplicated = []
        seen_positions = set()
        
        for entity in sorted_entities:
            # Create position key with tolerance (group nearby positions)
            position_key = (
                entity.entity_type,
                entity.start // 5,  # Group positions within 5 chars
                entity.end // 5
            )
            
            if position_key not in seen_positions:
                deduplicated.append(entity)
                seen_positions.add(position_key)
        
        duplicates_removed = len(entities) - len(deduplicated)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate entities from overlapping regions")
        
        return deduplicated

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
        
        Automatically uses chunking for large documents to handle spaCy's
        max_length limit. Documents larger than chunk_size are split into
        overlapping chunks, processed separately, and deduplicated.
        
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
                logger.info(f"Text length ({len(text):,} chars) exceeds chunk size ({self.chunk_size:,}), using chunking")
                
                # Create chunks
                chunks = self.create_chunks(text)
                
                # Process chunks
                all_entities = self.process_chunks(chunks, language, country)
                
                # Deduplicate entities from overlapping regions
                results = self.deduplicate_entities(all_entities)
                
                # Resolve overlapping entities
                resolved = self._resolve_overlapping_entities(results)
                
                logger.info(f"Detected {len(resolved)} PII entities for country={country} (chunked)")
                return resolved
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
                logger.info(f"Detected {len(resolved)} PII entities for country={country}")
                return resolved
                
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
        """Resolve overlapping entities by prioritizing highest score."""
        if not entities:
            return []
        
        # Sort by position first, then by score (highest first)
        sorted_ents = sorted(entities, key=lambda x: (x.start, x.end, -x.score))
        
        resolved: List[RecognizerResult] = []
        for ent in sorted_ents:
            # Check if this entity overlaps with any already resolved entity
            overlaps = [r for r in resolved if ent.start < r.end and ent.end > r.start]
            
            if not overlaps:
                # No overlap, add it
                resolved.append(ent)
            else:
                # There's overlap - keep the one with higher score
                for overlap in overlaps:
                    if ent.score > overlap.score:
                        # Replace lower score with higher score
                        resolved.remove(overlap)
                        resolved.append(ent)
                        break
        
        return sorted(resolved, key=lambda x: x.start)


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
