import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="testuser", password="testpass123")
    return user

@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    return client