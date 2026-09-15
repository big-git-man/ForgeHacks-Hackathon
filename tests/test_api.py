from fastapi.testclient import TestClient

from src.api import app
from src.application import AnalysisResponse
from src.schemas import ProjectIdea


class FakeApplicationService:
    def analyze(self, problem):
        return AnalysisResponse(
            problem=problem,
            status="completed",
            result=ProjectIdea(
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
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint(monkeypatch):
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

    assert data["problem"] == (
        "How can we reduce food waste?"
    )
    assert data["status"] == "completed"
    assert data["result"]["title"] == "Test Project"
