from src.request_context import (
    create_request_id,
    elapsed_ms,
    get_request_id,
    set_request_id,
    start_timer,
)


def test_request_id_lifecycle():
    request_id = create_request_id()

    assert request_id
    assert get_request_id() is None

    set_request_id(request_id)

    assert get_request_id() == request_id


def test_timer_returns_elapsed_time():
    start = start_timer()
    elapsed = elapsed_ms(start)

    assert elapsed >= 0
