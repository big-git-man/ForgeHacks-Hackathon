from src.request_context import (
    create_request_id,
    elapsed_ms,
    get_request_id,
    set_request_id,
    start_timer,
)


def test_request_id_generation():
    request_id = create_request_id()

    assert request_id
    assert len(request_id) == 36


def test_request_context_storage():
    set_request_id("test-request-id")

    assert get_request_id() == "test-request-id"


def test_timer_returns_non_negative_duration():
    start = start_timer()

    duration = elapsed_ms(start)

    assert duration >= 0
