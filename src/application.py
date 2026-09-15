from dataclasses import dataclass
from typing import Any


@dataclass
class AnalysisResponse:
    problem: str
    status: str
    result: Any


class ApplicationService:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def analyze(self, problem: str) -> AnalysisResponse:
        if not isinstance(problem, str):
            raise TypeError("Problem must be a string.")

        problem = problem.strip()

        if not problem:
            raise ValueError("Problem cannot be empty.")

        result = self.orchestrator.analyze_problem(problem)

        return AnalysisResponse(
            problem=problem,
            status="completed",
            result=result,
        )
