from src.metrics import (
    LLMCallMetrics,
    Metrics,
    RequestMetrics,
    ToolCallMetrics,
)


def test_request_average_latency():
    metrics = RequestMetrics(
        total_requests=2,
        total_latency_ms=100.0,
    )

    assert metrics.average_latency_ms == 50.0


def test_zero_request_latency():
    metrics = RequestMetrics()

    assert metrics.average_latency_ms == 0.0


def test_llm_average_latency():
    metrics = LLMCallMetrics(
        total_calls=4,
        total_latency_ms=200.0,
    )

    assert metrics.average_latency_ms == 50.0


def test_tool_average_latency():
    metrics = ToolCallMetrics(
        total_calls=5,
        total_latency_ms=250.0,
    )

    assert metrics.average_latency_ms == 50.0


def test_metrics_are_independent():
    first = Metrics()
    second = Metrics()

    first.requests.total_requests = 10

    assert second.requests.total_requests == 0
