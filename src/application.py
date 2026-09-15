from dataclasses import dataclass

from src.schemas import ProjectIdea


@dataclass
class AnalysisResponse:
    problem: str
    status: str
    result: ProjectIdea


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

        if not isinstance(result, ProjectIdea):
            result = ProjectIdea.model_validate(result)

        return AnalysisResponse(
            problem=problem,
            status="completed",
            result=result,
        )
