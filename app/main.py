"""Главный модуль приложения."""

from fastapi import FastAPI
from app.routes import convert

app = FastAPI(
    title="File Converter API",
    description="Конвертирует CSV, JSON, XML друг в друга",
    version="1.0.0",
)

app.include_router(convert.router)


"""@app.get("/")
def root():
    return {
        "message": "Добро пожаловать! Используйте POST /convert/",
        "example": "curl -F 'file=@data.csv' -F 'target_format=xml' http://localhost:8000/convert/",
    }"""
