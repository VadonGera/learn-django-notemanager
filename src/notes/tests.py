import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from notes.models import Note

User = get_user_model()


# ===== Fixtures =====


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


# ===== Model Tests =====


@pytest.mark.django_db
def test_note_str_representation():
    """Тест для модели Note. Создание заметки"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    note = Note.objects.create(
        title="Test Note", description="Test description", user=user
    )
    assert str(note) == "Test Note"


@pytest.mark.django_db
def test_note_creation():
    """Тест для модели Note. Представление заметки"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    note = Note.objects.create(
        title="Test Note", description="Test description", user=user
    )
    assert note.title == "Test Note"
    assert note.description == "Test description"
    assert note.user == user
    assert note.created_at is not None
    assert note.updated_at is not None


# ===== API Tests =====


@pytest.mark.django_db
def test_list_notes(auth_client, test_user):
    """Проверка списка заметок, принадлежащих пользователю"""
    Note.objects.create(title="Note 1", description="Description 1", user=test_user)
    Note.objects.create(title="Note 2", description="Description 2", user=test_user)

    response = auth_client.get("/notes/api/notes/")
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_create_note_success(auth_client):
    """Проверка создания заметки для аутентифицированного пользователя"""
    payload = {"title": "New Note", "description": "New Description"}
    response = auth_client.post("/notes/api/notes/", payload)
    assert response.status_code == 201
    assert response.data["title"] == payload["title"]
    assert response.data["description"] == payload["description"]


@pytest.mark.django_db
def test_create_note_unauthenticated(api_client):
    """Проверка создания заметки для неаутентифицированного пользователя"""
    payload = {"title": "New Note", "description": "New Description"}
    response = api_client.post("/notes/api/notes/", payload)
    assert response.status_code == 403  # Проверка для 403 вместо 401


@pytest.mark.django_db
def test_update_note(auth_client, test_user):
    """Проверка обновления заметки"""
    note = Note.objects.create(
        title="Old Title", description="Old Description", user=test_user
    )
    payload = {"title": "Updated Title", "description": "Updated Description"}

    response = auth_client.put(f"/notes/api/notes/{note.id}/", payload)
    assert response.status_code == 200
    assert response.data["title"] == payload["title"]
    assert response.data["description"] == payload["description"]


@pytest.mark.django_db
def test_delete_note_success(auth_client, test_user):
    """Проверка удаления заметки"""
    note = Note.objects.create(
        title="Note to delete", description="Some description", user=test_user
    )
    response = auth_client.delete(f"/notes/api/notes/{note.id}/")
    assert response.status_code == 204
    assert Note.objects.filter(id=note.id).count() == 0
