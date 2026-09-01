"""
Health check endpoint.

Проста, "нешумна" перевірка того, що застосунок запущений і відповідає на HTTP-запити,
без звернень до бази даних чи інших сервісів. Такий endpoint зазвичай використовують
хостинг-платформи (Render, Koyeb тощо) та orchestration-системи, щоб автоматично визначати,
чи застосунок живий (liveness check), і саме його варто перевірити першим після deployment.
"""

from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    """Повертає статус застосунку та назву поточного середовища (app_env)."""
    return {"status": "ok", "environment": settings.app_env}
