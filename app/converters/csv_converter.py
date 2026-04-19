"""Конвертер для CSV."""

import pandas as pd
from io import StringIO, BytesIO
from .base import BaseConverter


class CSVConverter(BaseConverter):
    """Работа с CSV файлами."""

    def to_intermediate(self, file_content: bytes) -> list[dict]:
        content_str = file_content.decode("utf-8")
        df = pd.read_csv(StringIO(content_str))
        return df.to_dict(orient="records")

    def from_intermediate(self, data: list[dict]) -> bytes:
        df = pd.DataFrame(data)
        output = StringIO()
        df.to_csv(output, index=False)
        return output.getvalue().encode("utf-8")
