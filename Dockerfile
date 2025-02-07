FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Обновляем список пакетов и устанавливаем утилиты
RUN apt-get update && \
    apt-get install -y wget gnupg2 lsb-release

# 2. Добавляем официальный репозиторий PostgreSQL
RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# 3. Добавляем ключ репозитория PostgreSQL
RUN wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# 4. Обновляем список пакетов с новым репозиторием
RUN apt-get update

# 5. Устанавливаем PostgreSQL клиент (включает pg_dump)
RUN apt-get install -y postgresql-client-16

# 6. Копируем файл зависимостей Python
COPY req.txt .

# 7. Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r req.txt

# 8. Копируем исходный код приложения
COPY . .
