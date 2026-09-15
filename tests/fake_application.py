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
