from fastapi.testclient import TestClient
from app.main import app
import pytest


@pytest.fixture
def client():
    return TestClient(app)

# client = TestClient(app)


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser6",
            "email": "test6@example.com",
            "password": "testpass6"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser6"
    assert data["email"] == "test6@example.com"
    assert "id" in data


def test_login_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test6@example.com",
            "password": "testpass6"
        }
    )

    # assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

