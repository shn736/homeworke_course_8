FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
# RUN apt-get update && apt-get install -y \\\\
#     gcc \\\\
#     libpq-dev \\\\
#     && apt-get clean \\\\
#     && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Определяем переменные окружения
ARG SECRET_KEY
ARG CELERY_BROKER_URL
ARG CELERY_BACKEND

ENV SECRET_KEY=$SECRET_KEY
ENV CELERY_BROKER_URL=$CELERY_BROKER_URL
ENV CELERY_BACKEND=$CELERY_BACKEND

RUN    docker build -t my_app \
          --build-arg SECRET_KEY=$(grep SECRET_KEY .env | cut -d '=' -f2) \
          --build-arg CELERY_BROKER_URL=$(grep CELERY_BROKER_URL .env | cut -d '=' -f2) \
          --build-arg CELERY_BACKEND=$(grep CELERY_BACKEND .env | cut -d '=' -f2) .

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]