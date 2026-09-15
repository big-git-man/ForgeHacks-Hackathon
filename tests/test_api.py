from fastapi.testclient import TestClient

from src.api import app
from tests.fake_application import FakeApplicationService


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint():
    app.state.application_service = (
        FakeApplicationService()
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/analyze",
            json={
                "problem": "How can we reduce food waste?"
            },
        )

        assert response.status_code == 200, (
            f"Unexpected response: {response.text}"
        )

        data = response.json()

        assert data["problem"] == (
            "How can we reduce food waste?"
        )
        assert data["status"] == "completed"
        assert data["result"]["title"] == "Test Project"
        assert data["result"]["solution"] == (
            "A test solution."
        )
        assert data["result"]["impact"] == (
            "Useful impact."
        )

    finally:
        if hasattr(
            app.state,
            "application_service",
        ):
            del app.state.application_service
