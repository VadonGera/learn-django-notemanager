https://chatgpt.com/g/g-cKXjWStaE-python/c/672f7654-5d8c-800b-9cf5-b95c68696352
https://chatgpt.com/g/g-cKXjWStaE-python/c/672e8ce9-3e08-800b-bea7-990d23907ab5

[Notes](https://chatgpt.com/g/g-cKXjWStaE-python/c/672e8ce9-3e08-800b-bea7-990d23907ab5)

[Users](https://chatgpt.com/g/g-cKXjWStaE-python/c/672f7654-5d8c-800b-9cf5-b95c68696352)

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


    pip install pytest pytest-django pytest-cov coverage

```shell
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = project_name.settings
python_files = tests.py test_*.py *_tests.py

```
    pytest --cov=notes --cov=users --cov-report=html

```shell
coverage run -m pytest
coverage report

```