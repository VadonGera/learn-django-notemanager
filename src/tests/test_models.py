import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    """Тест для CustomUser модели. Создание пользователя с обязательными полями"""
    user = User.objects.create_user(username="testuser", password="testpass123")
    assert user.username == "testuser"
    assert user.check_password("testpass123")


@pytest.mark.django_db
def test_create_user_with_phone_and_address():
    """Тест для CustomUser модели. Создание пользователя с дополнительными полями"""
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
        phone="123456789",
        address="Test Address",
    )
    assert user.phone == "123456789"
    assert user.address == "Test Address"
