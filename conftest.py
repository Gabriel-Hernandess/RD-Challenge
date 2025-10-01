import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture(scope="session")
def test_user(django_db_setup, django_db_blocker):
    """Cria um usuário de teste uma vez por sessão."""
    with django_db_blocker.unblock():
        user, _ = User.objects.get_or_create(username="testuser")
        user.set_password("testpass123")
        user.save()
    return user

@pytest.fixture
def auth_client(test_user):
    """Client autenticado com o usuário de teste."""
    client = APIClient()
    # Aqui você pode usar force_authenticate ou login via endpoint
    client.force_authenticate(user=test_user)
    return client