import pytest
from pydantic import ValidationError

from src.api_schemas import ProblemRequest


def test_problem_request_accepts_valid_problem():
    request = ProblemRequest(
        problem="Reduce food waste"
    )

    assert request.problem == "Reduce food waste"


def test_problem_request_rejects_empty_problem():
    with pytest.raises(ValidationError):
        ProblemRequest(problem="")


def test_problem_request_rejects_oversized_problem():
    with pytest.raises(ValidationError):
        ProblemRequest(
            problem="x" * 5001
        )
