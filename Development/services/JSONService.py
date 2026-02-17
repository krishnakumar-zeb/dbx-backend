"""JSON Service – mask PII in JSON files recursively."""
from fastapi import UploadFile
from typing import Dict, Any
import json

from services.BaseService import BaseService
from utility.exceptions import FileValidationException, DocumentProcessingException


class JSONService(BaseService):

    def _validate(self, document: UploadFile) -> None:
        fn = (document.filename or "").lower()
        if not fn.endswith(".json"):
            raise FileValidationException("File must be a .json file")

    def _extract_text(self, raw: bytes, filename: str) -> str:
        try:
            data = json.loads(raw.decode("utf-8"))
            return self._collect_strings(data)
        except Exception as e:
            raise DocumentProcessingException(f"JSON parse failed: {e}")

    def _collect_strings(self, obj: Any) -> str:
        """Recursively collect all string values."""
        if isinstance(obj, str):
            return obj + " "
        if isinstance(obj, dict):
            return "".join(self._collect_strings(v) for v in obj.values())
        if isinstance(obj, (list, tuple)):
            return "".join(self._collect_strings(i) for i in obj)
        return ""

    def _build_masked_output(self, raw, mapping, anonymized_text, out_path):
        """Replace PII strings inside the JSON structure."""
        try:
            data = json.loads(raw.decode("utf-8"))
            orig_text = self._collect_strings(data)
            from services.CSVService import CSVService
            replacements = CSVService._build_replacement_pairs(orig_text, anonymized_text)
            masked = self._mask_json(data, replacements)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(masked, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise DocumentProcessingException(f"JSON masking failed: {e}")

    def _mask_json(self, obj: Any, replacements: Dict[str, str]) -> Any:
        from services.CSVService import CSVService
        if isinstance(obj, str):
            return CSVService._apply_replacements(obj, replacements)
        if isinstance(obj, dict):
            return {k: self._mask_json(v, replacements) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [self._mask_json(i, replacements) for i in obj]
        return obj
