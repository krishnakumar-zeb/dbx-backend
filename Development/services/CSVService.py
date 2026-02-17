"""CSV Service – mask PII in CSV files cell-by-cell."""
from fastapi import UploadFile
from typing import Dict
import pandas as pd
import io

from services.BaseService import BaseService
from utility.exceptions import FileValidationException, DocumentProcessingException


class CSVService(BaseService):

    def _validate(self, document: UploadFile) -> None:
        fn = (document.filename or "").lower()
        if not fn.endswith(".csv"):
            raise FileValidationException("File must be a .csv file")

    def _extract_text(self, raw: bytes, filename: str) -> str:
        try:
            df = pd.read_csv(io.BytesIO(raw))
            # Concatenate all string cell values for PII scanning
            return " ".join(
                str(v) for v in df.values.flatten() if pd.notna(v)
            )
        except Exception as e:
            raise DocumentProcessingException(f"CSV parse failed: {e}")

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """Apply tag replacements to every cell in the CSV."""
        try:
            df = pd.read_csv(io.BytesIO(raw))
            # Build original->tag lookup from anonymized_text
            # We replace in each cell using the mapping tags
            from utility.PresidioUtility import decrypt_value
            # We need encryption key – but it's in the caller context.
            # Instead, do a simpler approach: replace known PII strings
            # with their tags across all cells.
            # The mapping is tag->{encrypted_value, ...}
            # We can't decrypt here, so use the anonymized_text approach:
            # re-parse the original text and the anonymized text to build
            # a direct original->tag map.
            orig_text = " ".join(
                str(v) for v in df.values.flatten() if pd.notna(v)
            )
            replacements = self._build_replacement_pairs(orig_text, anonymized_text)
            for col in df.columns:
                df[col] = df[col].apply(
                    lambda v: self._apply_replacements(str(v), replacements)
                    if pd.notna(v) else v
                )
            df.to_csv(out_path, index=False)
        except Exception as e:
            raise DocumentProcessingException(f"CSV masking failed: {e}")

    @staticmethod
    def _build_replacement_pairs(original: str, anonymized: str) -> Dict[str, str]:
        """
        Compare original and anonymized text to extract {original_value: tag} pairs.
        Uses a simple diff approach: find tags in anonymized text and map them
        back to the corresponding spans in the original.
        """
        import re
        pairs: Dict[str, str] = {}
        tag_pattern = re.compile(r"<[A-Z_]+_\d+>")
        tags = list(tag_pattern.finditer(anonymized))
        if not tags:
            return pairs

        # Walk through both texts to align
        anon_pos = 0
        orig_pos = 0
        for match in tags:
            tag_start = match.start()
            tag_end = match.end()
            tag = match.group()

            # Characters before this tag should be the same in both
            prefix_len = tag_start - anon_pos
            orig_pos += prefix_len
            anon_pos = tag_end

            # Find the original value: it's the text in original at orig_pos
            # that was replaced by the tag. We need to figure out its length.
            # Look ahead to the next common text after the tag.
            if anon_pos < len(anonymized):
                # Find next non-tag text
                next_tag = tag_pattern.search(anonymized, anon_pos)
                if next_tag:
                    next_common = anonymized[anon_pos:next_tag.start()]
                else:
                    next_common = anonymized[anon_pos:]

                if next_common and next_common in original[orig_pos:]:
                    end_idx = original.index(next_common, orig_pos)
                    orig_value = original[orig_pos:end_idx]
                    if orig_value.strip():
                        pairs[orig_value] = tag
                    orig_pos = end_idx
                else:
                    # Fallback: skip ahead
                    orig_pos += len(tag)
            else:
                # Tag is at the end
                orig_value = original[orig_pos:]
                if orig_value.strip():
                    pairs[orig_value] = tag
                orig_pos = len(original)

        return pairs

    @staticmethod
    def _apply_replacements(text: str, replacements: Dict[str, str]) -> str:
        """Apply all replacement pairs to text, longest match first."""
        for orig in sorted(replacements, key=len, reverse=True):
            text = text.replace(orig, replacements[orig])
        return text
