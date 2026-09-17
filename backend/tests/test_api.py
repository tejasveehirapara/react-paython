from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models.user import UserSession

payload = {
    "company_name": "Northstar Labs",
    "contact_person": "Avery Chen",
    "email": "avery@northstar.example.com",
    "phone": "+1 555 0100",
    "city": "Austin",
    "country": "United States",
}


def create_client(client: TestClient) -> int:
    response = client.post("/api/v1/clients", json=payload)
    assert response.status_code == 201
    return response.json()["data"]["id"]


def test_health(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "API is running", "data": None}


def test_create_client(client: TestClient):
    client_id = create_client(client)
    assert client_id == 1


def test_get_clients(client: TestClient):
    create_client(client)
    response = client.get("/api/v1/clients")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_client_by_id(client: TestClient):
    client_id = create_client(client)
    response = client.get(f"/api/v1/clients/{client_id}")
    assert response.status_code == 200
    assert response.json()["data"]["company_name"] == payload["company_name"]


def test_update_client(client: TestClient):
    client_id = create_client(client)
    response = client.put(f"/api/v1/clients/{client_id}", json={"company_name": "Northstar Studio"})
    assert response.status_code == 200
    assert response.json()["data"]["company_name"] == "Northstar Studio"


def test_delete_client(client: TestClient):
    client_id = create_client(client)
    response = client.delete(f"/api/v1/clients/{client_id}")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert client.get(f"/api/v1/clients/{client_id}").status_code == 404


def test_login_creates_user_session(client: TestClient, database_session):
    credentials = {"email": "admin@example.com", "password": "SecurePass123"}
    assert client.post("/api/v1/auth/register", json=credentials).status_code == 201

    response = client.post("/api/v1/auth/login", json=credentials)

    assert response.status_code == 200
    result = response.json()["data"]
    assert result["access_token"]
    session = database_session.scalar(select(UserSession).where(UserSession.id == result["session_id"]))
    assert session is not None
    assert session.token_hash != result["access_token"]
