"""Главный модуль приложения."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.routes import convert
import os

# Создаём папки если их нет
os.makedirs("app/static", exist_ok=True)
os.makedirs("app/templates", exist_ok=True)

app = FastAPI(
    title="File Converter API",
    description="Конвертирует CSV, JSON, XML друг в друга",
    version="1.0.0",
)

# Подключаем статические файлы (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключаем шаблоны (HTML)
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутер для API
app.include_router(convert.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Главная страница с интерфейсом пользователя."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api-info")
async def api_info():
    """Информация об API (для справки)."""
    return {
        "message": "API для конвертации файлов",
        "endpoints": {
            "POST /convert/": "Конвертация файла. Параметры: file (файл), target_format (csv/json/xml)"
        },
        "supported_formats": ["csv", "json", "xml"],
    }
