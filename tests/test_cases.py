# from dotenv import load_dotenv
# load_dotenv()

def test_create_case_retruns_expected_shape(client):
    response = client.post("/api/cases", json={"title": "Test case"})
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["id"], int)
    assert data["title"] == "Test case"
    assert data["status"] == "submitted"
    assert isinstance(data["created_at"], str)

def test_list_cases_contains_created_case(client):
    created = client.post("/api/cases", json={"title": "Another case"}).json()
    response = client.get("/api/cases")
    assert response.status_code == 200
    data = response.json()

    ids = [c["id"] for c in data]
    assert created["id"] in ids

def test_get_case_not_found_returns_404(client):
    res = client.get("/api/cases/999999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Case not found"

def test_update_case_status_invalid_value_returns_422(client):
    created = client.post("/api/cases", json={"title": "Status test"}).json()
    res = client.patch(f"/api/cases/{created['id']}/status", json={"status": "banana"})
    assert res.status_code == 422

def test_update_case_status_valid_value_updates_case(client):
    created = client.post("/api/cases", json={"title": "Status ok"}).json()
    res = client.patch(f"/api/cases/{created['id']}/status", json={"status": "processing"})
    assert res.status_code == 200
    assert res.json()["status"] == "processing"