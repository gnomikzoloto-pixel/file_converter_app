"""Утилиты для валидации."""
ALLOWED_EXTENSIONS = {'csv', 'json', 'xml'}


def validate_extension(filename: str) -> bool:
    """Проверяет, поддерживается ли расширение файла."""
    ext = filename.split('.')[-1].lower()
    return ext in ALLOWED_EXTENSIONS


def get_converter_class(ext: str):
    """Возвращает класс конвертера по расширению."""
    from app.converters.csv_converter import CSVConverter
    from app.converters.json_converter import JSONConverter
    from app.converters.xml_converter import XMLConverter

    mapping = {
        'csv': CSVConverter,
        'json': JSONConverter,
        'xml': XMLConverter
    }
    return mapping.get(ext.lower())