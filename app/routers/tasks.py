"""
Endpoint'и для роботи із задачами (Task).

Це базовий CRUD (Create, Read, Update, Delete) без:
  - фільтрації списку за query parameters;
  - окремого endpoint'у зі статистикою;
  - перевірки допустимості переходу статусу (status transition) у PATCH.

Ці три речі — саме те, що потрібно реалізувати самостійно за умовами тестового завдання
(див. README_TEST_TASK.md, Завдання 1-3).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _get_task_or_404(db: Session, task_id: int) -> Task:
    """Знаходить задачу за id або піднімає HTTPException(404), якщо її не існує."""
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    """Створює нову задачу зі статусом "todo" за замовчуванням."""
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskRead])
def list_tasks(status: Optional[str] = None, db: Session = Depends(get_db)) -> list[Task]:
    # 1. Створюємо змінну query
    query = db.query(Task)

    # 2. Оновлюємо її, якщо є статус
    if status is not None:
        query = query.filter(Task.status == status)

    # 3. Повертаємо саме змінну query (а не db.query)
    return list(query.order_by(Task.id).all())

@router.get("/stats")
def get_task_statistics(db: Session = Depends(get_db)):
    """
    Повертає статистику по задачах: загальну кількість та розбивку за статусами.
    (Виконання Завдання 2)
    """
    # Рахуємо всі задачі
    total = db.query(Task).count()

    # Рахуємо тільки ті, що todo
    todo_count = db.query(Task).filter(Task.status == "todo").count()

    # Рахуємо тільки ті, що done
    done_count = db.query(Task).filter(Task.status == "done").count()

    # Повертаємо красивий JSON-словник
    return {"total_tasks": total, "todo_tasks": todo_count, "done_tasks": done_count,}

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    """Повертає одну задачу за id або 404, якщо задачі з таким id не існує."""
    return _get_task_or_404(db, task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    """
    Частково оновлює задачу: змінює лише ті поля, які прийшли в тілі запиту.

    Увага: тут немає перевірки бізнес-правила допустимого переходу статусу
    (наприклад заборони переходу done -> todo) — це навмисно, дивись Завдання 3.
    """
    task = _get_task_or_404(db, task_id)


    # exclude_unset=True — беремо лише ті поля, які клієнт справді передав у запиті,
    # а не всі поля схеми зі значеннями None за замовчуванням.

    updates = payload.model_dump(exclude_unset=True)
    if "status" in updates:
        new_status = updates["status"]

        if task.status == "done" and new_status == "todo":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неможливо повернути виконану задачу (done) в статус 'todo'" )

    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """Видаляє задачу за id або повертає 404, якщо такої задачі немає."""
    task = _get_task_or_404(db, task_id)
    db.delete(task)
    db.commit()
