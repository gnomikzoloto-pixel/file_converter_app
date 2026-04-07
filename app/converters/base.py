"""Базовый класс для всех конвертеров."""
from abc import ABC, abstractmethod


class BaseConverter(ABC):
    """Абстрактный конвертер файлов."""

    @abstractmethod
    def to_intermediate(self, file_content: bytes) -> list[dict]:
        """Преобразует файл в промежуточный список словарей."""
        pass

    @abstractmethod
    def from_intermediate(self, data: list[dict]) -> bytes:
        """Преобразует промежуточный список словарей в целевой формат."""
        pass