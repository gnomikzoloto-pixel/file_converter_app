"""Конвертер для XML."""
import dicttoxml
import xmltodict
from .base import BaseConverter


class XMLConverter(BaseConverter):
    """Работа с XML."""

    def to_intermediate(self, file_content: bytes) -> list[dict]:
        content_str = file_content.decode('utf-8')
        data = xmltodict.parse(content_str)
        # Обычно корень содержит список записей
        root_key = list(data.keys())[0]
        records = data[root_key].get('record', [])
        if isinstance(records, dict):
            return [records]
        return records

    def from_intermediate(self, data: list[dict]) -> bytes:
        xml_data = {'root': {'record': data}}
        return dicttoxml.dicttoxml(xml_data, custom_root='root', attr_type=False)