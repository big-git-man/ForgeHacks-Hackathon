from src.metrics import Metrics


def test_request_metrics_update():
    metrics = Metrics()

    metrics.requests.total_requests += 1
    metrics.requests.successful_requests += 1
    metrics.requests.total_latency_ms += 100

    assert metrics.requests.total_requests == 1
    assert metrics.requests.successful_requests == 1
    assert metrics.requests.failed_requests == 0
    assert metrics.requests.average_latency_ms == 100


def test_llm_metrics_update():
    metrics = Metrics()

    metrics.llm.total_calls += 1
    metrics.llm.successful_calls += 1
    metrics.llm.total_latency_ms += 250

    assert metrics.llm.total_calls == 1
    assert metrics.llm.successful_calls == 1
    assert metrics.llm.failed_calls == 0
    assert metrics.llm.average_latency_ms == 250


def test_tool_metrics_update():
    metrics = Metrics()

    metrics.tools.total_calls += 1
    metrics.tools.successful_calls += 1
    metrics.tools.total_latency_ms += 25

    assert metrics.tools.total_calls == 1
    assert metrics.tools.successful_calls == 1
    assert metrics.tools.failed_calls == 0
    assert metrics.tools.average_latency_ms == 25
