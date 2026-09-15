from types import SimpleNamespace

from fastapi.testclient import TestClient

from src.api import app


class FakeApplicationService:
    def analyze(self, problem):
        return SimpleNamespace(
            problem=problem,
            status="completed",
            result=SimpleNamespace(
                title="Test Project",
                problem=problem,
                solution="A test solution.",
                impact="Useful impact.",
            ),
        )


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_analyze_validation():
    client = TestClient(app)

    response = client.post(
        "/analyze",
        json={"problem": ""},
    )

    assert response.status_code == 422


def test_analyze_success_with_mocked_service(monkeypatch):
    from src import api

    monkeypatch.setattr(
        api,
        "build_application_service",
        lambda: FakeApplicationService(),
    )

    client = TestClient(app)

    response = client.post(
        "/analyze",
        json={
            "problem": "How can we reduce food waste?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "completed"
    assert data["result"]["title"] == "Test Project"
    assert data["result"]["problem"] == (
        "How can we reduce food waste?"
    )
