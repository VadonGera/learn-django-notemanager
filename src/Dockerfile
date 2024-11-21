# Используем официальный образ Python в качестве базового
FROM python:3.12-alpine

# Мета данные
LABEL authors="horse"

## Аргументы сборки
#ARG SECRET_KEY
#ARG ALLOWED_HOSTS
#
#ARG SQL_DATABASE
#ARG SQL_USER
#ARG SQL_PASSWORD
#ARG SQL_PORT
#ARG DATABASE
#
#ARG DJANGO_SUPERUSER_USERNAME
#ARG DJANGO_SUPERUSER_EMAIL
#ARG DJANGO_SUPERUSER_PASSWORD
#
## Установка переменных окружения внутри контейнера
#ENV SECRET_KEY=$SECRET_KEY
#ENV ALLOWED_HOSTS=$ALLOWED_HOSTS
#
#ENV SQL_DATABASE=$SQL_DATABASE
#ENV SQL_USER=$SQL_USER
#ENV SQL_PASSWORD=$SQL_PASSWORD
#ENV SQL_PORT=$SQL_PORT
#ENV DATABASE=$DATABASE
#
#ENV DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME
#ENV DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL
#ENV DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD

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
