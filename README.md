# Task Management API — базовий проєкт для тестового завдання

Це базовий (стартовий) **FastAPI**-застосунок: невеликий REST API для керування задачами
(Tasks) з базовим CRUD (Create, Read, Update, Delete), моделлю даних та підключенням до бази
даних. Він служить вхідною точкою для тестового завдання, описаного в `README_TEST_TASK.md`
(докладні підказки — у `README_DETAILED_GUIDE.md`).

## Технології

- [FastAPI](https://fastapi.tiangolo.com/) — web-framework для побудови API;
- [Uvicorn](https://www.uvicorn.org/) — ASGI-сервер, яким застосунок запускається локально;
- [SQLAlchemy](https://docs.sqlalchemy.org/) (ORM) + [SQLite](https://www.sqlite.org/) — модель
  даних та зберігання (файл `app.db`, з'являється автоматично при першому запуску);
- [Pydantic](https://docs.pydantic.dev/) — схеми валідації запитів/відповідей;
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — конфігурація
  через environment variables;
- [pytest](https://docs.pytest.org/) + [httpx](https://www.python-httpx.org/) (через
  `fastapi.testclient.TestClient`) — тести.

## Структура проєкту

```
app/
├── main.py            # створення FastAPI-застосунку, підключення роутерів
├── config.py          # налаштування (Settings) через environment variables
├── database.py        # SQLAlchemy engine, сесії, dependency get_db
├── models.py           # ORM-модель Task, enum'и TaskStatus / TaskPriority
├── schemas.py           # Pydantic-схеми запитів/відповідей (TaskCreate, TaskUpdate, TaskRead)
└── routers/
    ├── health.py         # GET /health
    └── tasks.py            # CRUD-endpoint'и для задач
tests/                    # тести pytest для вже реалізованого функціоналу
```

## Як запустити локально

```bash
# 1. Створити та активувати virtualenv (якщо ще не створено)
python3 -m venv .venv
source .venv/bin/activate

# 2. Встановити залежності
pip install -r requirements.txt

# 3. (опційно) скопіювати приклад env-файлу
cp .env.example .env

# 4. Запустити застосунок
uvicorn app.main:app --reload
```

Після запуску:

- Swagger UI (інтерактивна документація API): http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

## Наявні endpoint'и

| Method | URL              | Опис                                             |
|--------|------------------|---------------------------------------------------|
| GET    | `/health`        | перевірка, що застосунок живий                     |
| POST   | `/tasks`         | створити нову задачу (статус за замовчуванням `todo`) |
| GET    | `/tasks`         | список усіх задач (без фільтрів)                    |
| GET    | `/tasks/{id}`    | одна задача за id (або 404)                         |
| PATCH  | `/tasks/{id}`    | часткове оновлення задачі (без правила переходу статусу) |
| DELETE | `/tasks/{id}`    | видалити задачу (або 404)                           |

Перевірити вручну, наприклад:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "priority": "high"}'

curl http://127.0.0.1:8000/tasks
```

## Тести

```bash
pytest
```

Тести покривають лише той функціонал, що вже реалізований у цьому базовому проєкті.

## Що потрібно зробити далі (тестове завдання)

Це навмисно **не повний** застосунок — три речі з Backend-частини завдання й усі DevOps-кроки
залишені для самостійного виконання. Повний опис — у `README_TEST_TASK.md` та
`README_DETAILED_GUIDE.md`. Коротко, чого тут свідомо немає:

**Backend:**
1. Фільтрація `GET /tasks` за query parameters (наприклад `?status=` та/або `?priority=`).
2. Новий endpoint на основі наявних даних (наприклад `GET /tasks/stats`).
3. Бізнес-правило: перевірка допустимого переходу статусу задачі в `PATCH /tasks/{id}`
   (наприклад заборона переходу `done -> todo`).

**DevOps:**
- Git repository та публікація в GitHub (проєкт ще не під контролем версій);
- Dockerfile для запуску застосунку в контейнері;
- CI (наприклад GitHub Actions): встановлення залежностей, `pytest`, збірка Docker image;
- Deployment на публічний hosting (наприклад Render чи Koyeb) з публічним URL;
- CD: автоматичний деплой після успішного CI;
- Environment variables / secrets для production-конфігурації (шаблон уже є в `app/config.py`
  та `.env.example` — production-значення `DATABASE_URL` тощо мають прийти через середовище
  хостингу, а не через код).
