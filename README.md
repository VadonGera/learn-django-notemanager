    py -m venv .venv
    .venv\Scripts\activate.bat

    py -m pip install --upgrade pip

    pip install -r requirements.txt
    pip freeze > requirements.txt

    django-admin startproject app .

    python manage.py startapp tree

    python manage.py runserver 127.0.0.1:8001 --settings=app.settings


    docker compose up -d
    docker compose down

    python manage.py makemigrations tree
    python manage.py migrate

    python manage.py createsuperuser --username horse --email vadongera@gmail.com