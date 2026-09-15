from pydantic import BaseModel

from src.schemas import ProjectIdea


class ProblemRequest(BaseModel):
    problem: str


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    detail: str


class AnalysisResponse(BaseModel):
    problem: str
    status: str
    result: ProjectIdea
