"""Конвертер для JSON."""
import json
from .base import BaseConverter


class JSONConverter(BaseConverter):
    """Работа с JSON."""

    def to_intermediate(self, file_content: bytes) -> list[dict]:
        data = json.loads(file_content.decode('utf-8'))
        if isinstance(data, dict):
            return [data]
        return data

    def from_intermediate(self, data: list[dict]) -> bytes:
        return json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')