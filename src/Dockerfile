# Используем официальный образ Python в качестве базового
FROM python:3.12-alpine

# Мета данные
LABEL authors="horse"

# Обновляем apk и устанавливаем необходимые зависимости
# При использовании python:3.12-slim работаем с apt-get
# В python:3.12-alpine нет bash
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    bash
RUN apk add dos2unix

# Предотвращаем создание .pyc файлов, экономим пространство
ENV PYTHONDONTWRITEBYTECODE=1
# Отключает буферизацию стандартного вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /my_application

RUN pip install --upgrade pip
# Копируем requirements.txt и устанавливаем Python зависимости отдельным слоем
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы директории src в контейнер следующим слоем
COPY . .
# Теперь структура выглядит так: '/my_application/*.*'

# Конвертируем файл entrypoint.sh в Unix-формат строк (LF). Иначе ругается на рабочем компе.
RUN dos2unix entrypoint.sh
# COPY entrypoint.sh /my_application/entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
