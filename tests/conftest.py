"""
Спільні фікстури pytest для тестів API.

Головна ідея — override (перевизначення) FastAPI-залежності get_db, щоб тести працювали
з окремою тестовою базою даних (SQLite в оперативній пам'яті), а не з "робочим" app.db.
Так тести залишаються швидкими, ізольованими одне від одного та не псують локальні дані.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# StaticPool + check_same_thread=False потрібні, щоб усі з'єднання в межах одного тесту
# бачили ту саму in-memory SQLite-базу (за замовчуванням кожне нове з'єднання до
# "sqlite:///:memory:" створює свою окрему, порожню базу).
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture()
def client():
    """FastAPI TestClient зі свіжою (порожньою) тестовою базою даних для кожного тесту."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
