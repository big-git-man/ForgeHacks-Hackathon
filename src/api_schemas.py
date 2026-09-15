from typing import Any

from pydantic import BaseModel, Field


class ProblemRequest(BaseModel):
    problem: str = Field(
        min_length=1,
        max_length=5000,
    )


class AnalysisResult(BaseModel):
    title: str
    problem: str
    solution: str
    impact: str


class AnalysisResponse(BaseModel):
    problem: str
    status: str
    result: AnalysisResult


class ErrorResponse(BaseModel):
    error: str
    detail: str


class HealthResponse(BaseModel):
    status: str
