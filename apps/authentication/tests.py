import pytest

@pytest.mark.django_db
def test_login_success(auth_client):
    response = auth_client.post(
        "/auth/login/",
        {"username": "testuser", "password": "testpass123"},
        format="json"
    )
    
    assert response.status_code == 200
    assert response.data["success"] is True
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies

@pytest.mark.django_db
def test_login_fail(auth_client):
    # Logout para usar client sem autenticação
    auth_client.logout()
    response = auth_client.post("/auth/login/", {"username": "wrong", "password": "wrong"}, format="json")
    
    assert response.status_code == 400
    assert response.data["success"] is False

@pytest.mark.django_db
def test_logout(auth_client):
    response = auth_client.post("/auth/logout/")
    
    assert response.status_code == 200
    assert response.data["success"] is True