"""
ORM-моделі застосунку.

Тут описана єдина сутність — задача (Task). Поля status і priority реалізовані як
Python Enum (перелік) — це не дозволяє записати в базу довільний рядок замість одного
з наперед визначених значень.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskStatus(str, enum.Enum):
    """Можливі статуси задачі. Життєвий цикл (за задумом): TODO -> IN_PROGRESS -> DONE."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, enum.Enum):
    """Можливі рівні пріоритету задачі."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def _utcnow() -> datetime:
    """Поточний час у UTC — окрема функція, щоб SQLAlchemy викликав її для кожного нового рядка."""
    return datetime.now(timezone.utc)


class Task(Base):
    """Таблиця `tasks` — одна задача в системі."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus), nullable=False, default=TaskStatus.TODO
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SqlEnum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )
