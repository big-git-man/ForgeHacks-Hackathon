from fastapi.testclient import TestClient

from src.api import app
from tests.fake_application import FakeApplicationService


def test_health_returns_request_id():
    app.state.application_service = (
        FakeApplicationService()
    )

    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    request_id = response.headers.get(
        "X-Request-ID"
    )

    assert request_id
    assert len(request_id) > 10


def test_analyze_returns_request_id():
    app.state.application_service = (
        FakeApplicationService()
    )

    client = TestClient(app)

    response = client.post(
        "/analyze",
        json={
            "problem": "Students need affordable meals."
        },
    )

    assert response.status_code == 200

    request_id = response.headers.get(
        "X-Request-ID"
    )

    assert request_id
    assert len(request_id) > 10
