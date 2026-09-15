from pydantic import BaseModel, Field

from src.schemas import ProjectIdea


class ProblemRequest(BaseModel):
    problem: str = Field(
        min_length=1,
        max_length=5000,
    )


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    detail: str
    request_id: str | None = None


class AnalysisResponse(BaseModel):
    problem: str
    status: str
    result: ProjectIdea
