# Используем официальный образ Python в качестве базового
FROM python:3.12-slim

# Мета данные
LABEL authors="horse"

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Предотвращаем создание .pyc файлов, экономим пространство
ENV PYTHONDONTWRITEBYTECODE=1
# Отключает буферизацию стандартного вывода
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# Копируем все файлы директории src в контейнер
COPY . ./
# Теперь структура выглядит так: '/usr/src/app/*.*'
