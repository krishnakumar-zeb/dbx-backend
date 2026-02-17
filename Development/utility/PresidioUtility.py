"""
Presidio utility for PII detection and anonymization.
Supports country-specific PII entity detection with custom regex recognizers.
"""
from presidio_analyzer import AnalyzerEngine, RecognizerResult, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from typing import List, Dict, Optional
import base64
import os
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from utility.exceptions import PresidioException
from utility.country_pii_config import (
    get_entities_for_country,
    get_regex_patterns_for_country,
    DEFAULT_COUNTRY,
)
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

    def __init__(self):
        try:
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            logger.info("Presidio engines initialised")
        except Exception as e:
            raise PresidioException(f"Failed to initialise Presidio: {e}")

    # ------------------------------------------------------------------
    # Country-specific recognizer registration
    # ------------------------------------------------------------------
    def _register_country_recognizers(self, country: str) -> None:
        """Add regex-based PatternRecognizers for *country* to the registry."""
        registry = self.analyzer.registry
        patterns = get_regex_patterns_for_country(country)
        for entity_name, regex, context, score in patterns:
            recognizer_name = f"{country}_{entity_name}_recognizer"
            # Avoid duplicate registration
            existing = [r.name for r in registry.recognizers]
            if recognizer_name in existing:
                continue
            pat = Pattern(name=entity_name, regex=regex.pattern, score=score)
            rec = PatternRecognizer(
                supported_entity=entity_name,
                name=recognizer_name,
                patterns=[pat],
                context=context,
                supported_language="en",
            )
            registry.add_recognizer(rec)

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------
    def detect_pii(
        self,
        text: str,
        language: str = "en",
        country: str = DEFAULT_COUNTRY,
    ) -> List[RecognizerResult]:
        """Detect PII entities using country-specific rules."""
        try:
            if not text or not text.strip():
                return []

            self._register_country_recognizers(country)
            entities = get_entities_for_country(country)

            results = self.analyzer.analyze(
                text=text,
                language=language,
                entities=entities,
            )

            filtered = [e for e in results if e.score >= 0.5]
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
        if not entities:
            return []
        sorted_ents = sorted(entities, key=lambda x: (x.start, -x.score))
        resolved: List[RecognizerResult] = []
        for ent in sorted_ents:
            if not any(
                ent.start < r.end and ent.end > r.start for r in resolved
            ):
                resolved.append(ent)
        return resolved


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
