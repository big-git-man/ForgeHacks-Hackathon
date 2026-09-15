from fastapi.testclient import TestClient

from src.api import app
from tests.fake_application import FakeApplicationService


def test_health_returns_request_id():
    original = getattr(
        app.state,
        "application_service",
        None,
    )

    try:
        app.state.application_service = FakeApplicationService()

        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

        request_id = response.headers.get("X-Request-ID")

        assert request_id
        assert len(request_id) == 36

    finally:
        if original is None:
            if hasattr(app.state, "application_service"):
                del app.state.application_service
        else:
            app.state.application_service = original


def test_analyze_returns_request_id():
    original = getattr(
        app.state,
        "application_service",
        None,
    )

    try:
        app.state.application_service = FakeApplicationService()

        client = TestClient(app)

        response = client.post(
            "/analyze",
            json={
                "problem": "Students struggle to find study resources."
            },
        )

        assert response.status_code == 200

        request_id = response.headers.get("X-Request-ID")

        assert request_id
        assert len(request_id) == 36

    finally:
        if original is None:
            if hasattr(app.state, "application_service"):
                del app.state.application_service
        else:
            app.state.application_service = original
