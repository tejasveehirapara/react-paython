from fastapi.testclient import TestClient

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
