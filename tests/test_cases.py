from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_case():
    response = client.post("/api/cases", json={"title": "Test case"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test case"
    assert data["status"] == "submitted"
    assert "id" in data

def test_list_cases_retirns_list():
    client.post("/api/cases", json={"title": "Another case"})
    response = client.get("/api/cases")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_case_not_found():
    response = client.get("/api/cases/999999")
    assert response.status_code == 404