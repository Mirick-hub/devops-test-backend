"""
Точка входу FastAPI-застосунку.

Запуск локально (з кореня проєкту, з активованим virtualenv):

    uvicorn app.main:app --reload

Uvicorn — ASGI-сервер (Asynchronous Server Gateway Interface): він приймає HTTP-запити
і передає їх у наш об'єкт `app`, а FastAPI вже сам маршрутизує їх у відповідні endpoint'и.
Після старту документація Swagger UI доступна на http://127.0.0.1:8000/docs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import health, tasks


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Lifespan — сучасний спосіб у FastAPI виконати код при старті й при завершенні роботи
    застосунку (замінює застарілий декоратор @app.on_event("startup")).

    Тут при старті створюються таблиці бази даних, якщо їх ще немає. У навчальному проєкті
    цього достатньо; у "великих" production-проєктах для зміни схеми бази даних зазвичай
    використовують окремий інструмент migrations (наприклад Alembic).
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Management API",
    description="Базовий FastAPI-застосунок для тестового завдання (Backend + DevOps).",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(tasks.router)
