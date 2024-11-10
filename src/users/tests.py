import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


# ===== Fixtures =====


@pytest.fixture
def api_client():
    return APIClient()


# ===== Model Tests =====


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


# ===== API Tests =====


@pytest.mark.django_db
def test_user_registration(api_client):
    """Тест представлений. Успешная регистрация пользователя"""
    url = reverse("user-register")
    data = {"username": "newuser", "password": "newpassword"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_user_list_accessible_to_admin(api_client):
    """Тест представлений. Доступ администратора к списку пользователей"""
    admin_user = User.objects.create_superuser(username="admin", password="adminpass")
    api_client.force_authenticate(user=admin_user)

    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_list_inaccessible_to_non_admin(api_client):
    """Тест представлений. Отказ доступа к списку пользователей для обычного пользователя"""
    normal_user = User.objects.create_user(username="user", password="userpass")
    api_client.force_authenticate(user=normal_user)

    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_can_update_own_profile(api_client):
    """Тест API. Возможность пользователя редактировать собственный профиль
    (изменять username нельзя)"""
    user = User.objects.create_user(username="testuser", password="testpass")
    api_client.force_authenticate(user=user)

    url = reverse("user-detail", args=[user.id])
    data = {"username": "updateduser", "phone": "987654321", "address": "New Address"}
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.username == "testuser"
    assert user.phone == "987654321"
    assert user.address == "New Address"


@pytest.mark.django_db
def test_user_cannot_update_other_user_profile(api_client):
    """Тест API. Запрет на редактирование чужого профиля для обычных пользователей"""
    user1 = User.objects.create_user(username="user1", password="pass1")
    user2 = User.objects.create_user(username="user2", password="pass2")
    api_client.force_authenticate(user=user1)

    url = reverse("user-detail", args=[user2.id])
    data = {"phone": "987654321"}
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_admin_can_update_any_user_profile(api_client):
    """Тест API. Возможность администратора редактировать профиль любого пользователя"""
    admin_user = User.objects.create_superuser(username="admin", password="adminpass")
    normal_user = User.objects.create_user(username="user", password="userpass")
    api_client.force_authenticate(user=admin_user)

    url = reverse("user-detail", args=[normal_user.id])
    data = {"address": "updated_address"}
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

    normal_user.refresh_from_db()
    assert normal_user.address == "updated_address"
