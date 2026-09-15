from fastapi import Request

from src.logger import get_logger
from src.request_context import (
    create_request_id,
    elapsed_ms,
    set_request_id,
    start_timer,
)


logger = get_logger("api")


async def request_logging_middleware(
    request: Request,
    call_next,
):
    request_id = create_request_id()
    set_request_id(request_id)

    start_time = start_timer()

    logger.info(
        "Request started | request_id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    duration_ms = elapsed_ms(start_time)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "Request completed | request_id=%s | status=%s | duration_ms=%.2f",
        request_id,
        response.status_code,
        duration_ms,
    )

    return response
