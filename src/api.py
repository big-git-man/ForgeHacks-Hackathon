from fastapi import FastAPI, HTTPException

from src.api_schemas import (
    AnalysisResponse,
    ErrorResponse,
    HealthResponse,
    ProblemRequest,
)
from src.application import ApplicationService
from src.llm_client import LLMClient
from src.orchestrator import AIOrchestrator


app = FastAPI(
    title="ForgeHacks AI API",
    version="0.2.0",
)


def build_application_service() -> ApplicationService:
    client = LLMClient()

    orchestrator = AIOrchestrator(
        llm_client=client,
    )

    return ApplicationService(
        orchestrator=orchestrator,
    )


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
    )


@app.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {
            "model": ErrorResponse,
        },
        500: {
            "model": ErrorResponse,
        },
    },
)
def analyze(
    request: ProblemRequest,
) -> AnalysisResponse:
    try:
        service = build_application_service()

        response = service.analyze(
            request.problem
        )

        return AnalysisResponse.model_validate(
            {
                "problem": response.problem,
                "status": response.status,
                "result": response.result.model_dump(),
            }
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Analysis service failed.",
        ) from exc
