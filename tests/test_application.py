from types import SimpleNamespace

from src.application import ApplicationService


class FakeOrchestrator:
    def analyze_problem(self, problem):
        return SimpleNamespace(
            title="Test Project",
            problem=problem,
            solution="A test solution.",
            impact="Useful impact.",
        )


def test_application_service_analyzes_problem():
    service = ApplicationService(
        FakeOrchestrator()
    )

    response = service.analyze(
        "Test problem"
    )

    assert response.problem == "Test problem"
    assert response.status == "completed"
    assert response.result.title == "Test Project"


def test_application_service_rejects_empty_problem():
    service = ApplicationService(
        FakeOrchestrator()
    )

    try:
        service.analyze("   ")
        assert False
    except ValueError as exc:
        assert str(exc) == "Problem cannot be empty."
