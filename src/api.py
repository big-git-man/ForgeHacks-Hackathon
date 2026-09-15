from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response

from src.api_schemas import (
    AnalysisResponse,
    ErrorResponse,
    HealthResponse,
    ProblemRequest,
)
from src.application import ApplicationService
from src.llm_client import LLMClient
from src.logger import get_logger
from src.metrics import metrics
from src.orchestrator import AIOrchestrator
from src.request_context import (
    create_request_id,
    elapsed_ms,
    set_request_id,
    start_timer,
)


logger = get_logger("api")


app = FastAPI(
    title="ForgeHacks AI API",
    version="0.3.0",
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


@app.middleware("http")
async def observability_middleware(
    request: Request,
    call_next,
) -> Response:
    request_id = create_request_id()
    set_request_id(request_id)

    start_time = start_timer()

    metrics.requests.total_requests += 1

    logger.info(
        "REQUEST START | "
        f"id={request_id} | "
        f"method={request.method} | "
        f"path={request.url.path}"
    )

    try:
        response = await call_next(request)

        latency = elapsed_ms(start_time)

        metrics.requests.total_latency_ms += latency

        if response.status_code < 400:
            metrics.requests.successful_requests += 1
        else:
            metrics.requests.failed_requests += 1

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "REQUEST END | "
            f"id={request_id} | "
            f"status={response.status_code} | "
            f"latency_ms={latency:.2f}"
        )

        return response

    except Exception:
        latency = elapsed_ms(start_time)

        metrics.requests.total_latency_ms += latency
        metrics.requests.failed_requests += 1

        logger.exception(
            "REQUEST ERROR | "
            f"id={request_id} | "
            f"latency_ms={latency:.2f}"
        )

        raise


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    return HealthResponse(
        status="healthy"
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
            request.problem
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
        logger.exception(
            "Analysis service failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Analysis service failed.",
        ) from exc
