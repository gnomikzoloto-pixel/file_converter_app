"""Конвертер для XML."""

import dicttoxml
import xmltodict
from xml.dom.minidom import parseString
from .base import BaseConverter


class XMLConverter(BaseConverter):
    """Работа с XML."""

    def to_intermediate(self, file_content: bytes) -> list[dict]:
        """Преобразует XML в list[dict]."""
        content_str = file_content.decode("utf-8")
        data = xmltodict.parse(content_str)

        # Ищем корневой элемент
        root_key = list(data.keys())[0]
        root_value = data[root_key]

        # Пытаемся найти список записей
        if isinstance(root_value, dict):
            # Ищем ключ, содержащий список
            for key in ["record", "item", "element", "row", "data", "root"]:
                if key in root_value:
                    if isinstance(root_value[key], list):
                        return root_value[key]
                    elif isinstance(root_value[key], dict):
                        return [root_value[key]]

            # Если нет явного списка, собираем все значения
            result = []
            for value in root_value.values():
                if isinstance(value, dict):
                    result.append(value)
                elif isinstance(value, list):
                    result.extend(value)
            if result:
                return result

            return [root_value]

        if isinstance(root_value, list):
            return root_value

        return [{root_key: root_value}]

    def from_intermediate(self, data: list[dict]) -> bytes:
        """Преобразует list[dict] в красивый XML."""
        if not data:
            return b'<?xml version="1.0" encoding="UTF-8"?>\n<root/>'

        # Конвертируем список словарей в XML
        xml_bytes = dicttoxml.dicttoxml(data, custom_root="root", attr_type=False)

        # Форматируем XML для красивого вывода
        try:
            dom = parseString(xml_bytes)
            pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8")
            # Убираем лишнюю пустую строку в начале
            pretty_xml = pretty_xml.decode("utf-8").strip()
            return pretty_xml.encode("utf-8")
        except Exception:
            # Если форматирование не удалось, возвращаем как есть
            return xml_bytes
