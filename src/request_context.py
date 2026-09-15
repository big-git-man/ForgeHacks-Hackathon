from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)


def create_request_id() -> str:
    return str(uuid4())


def set_request_id(request_id: str) -> None:
    _request_id.set(request_id)


def get_request_id() -> str | None:
    return _request_id.get()


def start_timer() -> float:
    return perf_counter()


def elapsed_ms(start_time: float) -> float:
    return (perf_counter() - start_time) * 1000
