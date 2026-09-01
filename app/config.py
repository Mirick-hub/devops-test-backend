"""
Конфігурація застосунку.

Використовує pydantic-settings (клас BaseSettings) — стандартний спосіб у FastAPI-екосистемі
читати налаштування з environment variables (та опційно з файлу .env для локальної розробки),
а не хардкодити значення в коді.

Це напряму знадобиться в DevOps-частині тестового завдання (Environment Variables & Secrets):
на своєму комп'ютері можна тримати .env-файл, а на хостингу (Render/Koyeb тощо) — виставити ті
самі змінні через панель налаштувань платформи, без зміни коду.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Налаштування застосунку, що читаються зі змінних середовища (environment variables)."""

    # URL підключення до бази даних у форматі SQLAlchemy (напр. "sqlite:///./app.db").
    # За замовчуванням — локальний файл SQLite, щоб застосунок запускався без додаткового
    # налаштування зовнішньої БД.
    database_url: str = "sqlite:///./app.db"

    # Довільна назва середовища (local/staging/production) — корисно бачити в /health
    # або в логах, щоб розрізняти, де саме запущено застосунок.
    app_env: str = "local"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Єдиний екземпляр налаштувань (singleton) — імпортується в інших модулях
# замість того, щоб кожного разу створювати новий Settings().
settings = Settings()
