from fastapi import Request
from fastapi.responses import JSONResponse

from src.logger import get_logger
from src.request_context import get_request_id


logger = get_logger("api_errors")


async def value_error_handler(
    request: Request,
    exc: ValueError,
) -> JSONResponse:
    request_id = get_request_id()

    logger.warning(
        "Validation error | request_id=%s | path=%s | detail=%s",
        request_id,
        request.url.path,
        str(exc),
    )

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
            "request_id": request_id,
        },
    )


async def generic_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    request_id = get_request_id()

    logger.exception(
        "Unhandled application error | request_id=%s | path=%s",
        request_id,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
            "request_id": request_id,
        },
    )
