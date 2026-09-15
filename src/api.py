from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="ForgeHacks AI API",
    version="0.1.0",
)


class ProblemRequest(BaseModel):
    problem: str


class HealthResponse(BaseModel):
    status: str


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    return HealthResponse(
        status="healthy"
    )


@app.post("/analyze")
def analyze(request: ProblemRequest):
    return {
        "problem": request.problem,
        "status": "received",
    }
