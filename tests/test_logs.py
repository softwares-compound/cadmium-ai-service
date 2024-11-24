from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_receive_log():
    response = client.post("/logs/", json={
        "id": "123",
        "org_id": "org_456",
        "app_id": "app_789",
        "message": "Test log message",
        "level": "info",
        "timestamp": "2024-11-24T10:00:00Z"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"
