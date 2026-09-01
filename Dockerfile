# Використовуємо легку версію Python
FROM python:3.11-slim

# Створюємо папку для проєкту всередині контейнера
WORKDIR /app

# Спочатку копіюємо і встановлюємо залежності (для швидкості)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Тепер копіюємо весь наш код
COPY . .

# Відкриваємо порт 8000
EXPOSE 8000

# Запускаємо сервер (змініть 'main:app' на 'app.main:app', якщо ваш файл main.py лежить у папці app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]