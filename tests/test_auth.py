from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser1",
            "email": "test1@example.com",
            "password": "testpass1"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser1"
    assert data["email"] == "test1@example.com"
    assert "id" in data
