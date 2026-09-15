from fastapi import FastAPI, HTTPException

from src.api_errors import (
    generic_error_handler,
    value_error_handler,
)
from src.api_middleware import request_logging_middleware
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
    version="0.3.0",
    description="Production-ready API foundation for ForgeHacks.",
)


app.middleware("http")(request_logging_middleware)

app.add_exception_handler(
    ValueError,
    value_error_handler,
)

app.add_exception_handler(
    Exception,
    generic_error_handler,
)


def build_application_service() -> ApplicationService:
    client = LLMClient()

    orchestrator = AIOrchestrator(
        llm_client=client,
    )

    return ApplicationService(
        orchestrator=orchestrator,
    )


def get_application_service() -> ApplicationService:
    service = getattr(
        app.state,
        "application_service",
        None,
    )

    if service is None:
        service = build_application_service()

    return service


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
        service = get_application_service()

        response = service.analyze(
            request.problem,
        )

        return AnalysisResponse(
            problem=response.problem,
            status=response.status,
            result=response.result,
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
