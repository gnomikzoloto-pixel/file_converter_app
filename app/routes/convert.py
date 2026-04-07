"""Маршруты для конвертации."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from app.utils.validators import validate_extension, get_converter_class

router = APIRouter()


@router.post("/convert/")
async def convert_file(file: UploadFile = File(...), target_format: str = "json"):
    """
    Конвертирует загруженный файл в указанный формат.
    Возвращает результат для просмотра в браузере.
    """
    if not validate_extension(file.filename):
        raise HTTPException(400, "Неподдерживаемый формат файла")

    source_ext = file.filename.split(".")[-1].lower()
    target_ext = target_format.lower()

    if source_ext == target_ext:
        raise HTTPException(400, "Исходный и целевой форматы совпадают")

    source_converter_class = get_converter_class(source_ext)
    target_converter_class = get_converter_class(target_ext)

    if not source_converter_class or not target_converter_class:
        raise HTTPException(400, "Неподдерживаемый формат конвертации")

    content = await file.read()

    try:
        source_converter = source_converter_class()
        intermediate = source_converter.to_intermediate(content)

        target_converter = target_converter_class()
        output_bytes = target_converter.from_intermediate(intermediate)

    except Exception as e:
        raise HTTPException(500, f"Ошибка конвертации: {str(e)}")

    # Определяем media_type для красивого отображения
    if target_ext == "json":
        media_type = "application/json"
    elif target_ext == "csv":
        media_type = "text/csv"
    else:
        media_type = "application/xml"

    return Response(
        content=output_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f"inline; filename=converted.{target_ext}"},
    )
