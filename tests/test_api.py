from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint():
    response = client.post(
        "/analyze",
        json={
            "problem": "Students need better study tools."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["problem"]
        == "Students need better study tools."
    )
    assert data["status"] == "received"
