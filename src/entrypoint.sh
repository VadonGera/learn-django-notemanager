#!/bin/bash
set -e

# Собираем статику
python manage.py collectstatic --noinput

# Выполняем миграции базы данных
python manage.py makemigrations
python manage.py migrate --noinput

# Создаем суперпользователя, если скрипт superuser.py существует
if [ -f "users/superuser.py" ]; then
    python manage.py shell < users/superuser.py
fi

# Запускаем Gunicorn
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3
