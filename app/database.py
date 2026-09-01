"""
Налаштування підключення до бази даних через SQLAlchemy (ORM — Object-Relational Mapping).

ORM дозволяє описувати таблиці бази даних як звичайні Python-класи (див. app/models.py)
і працювати з рядками таблиці як з об'єктами, без написання "сирого" SQL для типових операцій.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# connect_args потрібен лише для SQLite: за замовчуванням SQLite-драйвер дозволяє
# використовувати з’єднання тільки з того потоку, у якому воно було створене.
# FastAPI/Starlette можуть обробляти запити в різних потоках, тож цю перевірку відключаємо.
_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=_connect_args)

# Фабрика сесій (Session) — сесія в SQLAlchemy представляє собою одну "розмову" з базою
# даних (шаблон Unit of Work): у її межах відстежуються зміни об’єктів і виконується commit/rollback.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Базовий клас для всіх ORM-моделей (таблиць) застосунку."""


def get_db():
    """
    FastAPI dependency (механізм Dependency Injection), що надає endpoint'у сесію бази даних.

    Це генератор: код до `yield` виконується перед обробкою запиту (створення сесії),
    а код після `yield` — завжди після обробки запиту, навіть якщо в хендлері сталася помилка
    (сесія гарантовано закривається і не "протікає").
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
