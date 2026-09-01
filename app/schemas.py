"""
Pydantic-схеми (їх ще називають DTO — Data Transfer Object).

Це не ORM-моделі з app/models.py: схеми описують форму даних, які застосунок приймає
у тілі запиту (request body) і повертає у відповіді (response body), і саме на їхній основі
FastAPI автоматично виконує валідацію та будує документацію Swagger / OpenAPI.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """Дані, потрібні для створення нової задачі (POST /tasks)."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    priority: TaskPriority = TaskPriority.MEDIUM
    # status свідомо відсутній: нова задача завжди починається зі статусу "todo"
    # (значення за замовчуванням в ORM-моделі), клієнт не повинен його задавати напряму.


class TaskUpdate(BaseModel):
    """
    Дані для часткового оновлення задачі (PATCH /tasks/{task_id}).

    Усі поля опційні (Optional): клієнт передає лише ті поля, які хоче змінити.
    Обробник endpoint'у сам вирішує, які з переданих полів застосувати.
    """

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None


class TaskRead(BaseModel):
    """Форма задачі, яку API повертає клієнту у відповідях."""

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime

    # from_attributes=True дозволяє створювати цю Pydantic-схему прямо з ORM-об'єкта
    # Task (SQLAlchemy model instance), а не лише зі словника.
    model_config = ConfigDict(from_attributes=True)
