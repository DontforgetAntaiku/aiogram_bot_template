# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Установка необходимых пакетов для загрузки ключа и обновления репозитория
RUN apt-get update && apt-get install -y \
    lsb-release \
    curl \
    gnupg

# Загрузка ключа для репозитория Redis
RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

# Добавление репозитория Redis в список источников APT
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list

# Обновление списка пакетов и установка Redis
RUN apt-get update && apt-get install -y redis

# Копируем зависимости проекта и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Копируем исходный код проекта в контейнер
COPY . .

# Команда, которая будет запущена при старте контейнера
CMD ["python", "main.py"]
