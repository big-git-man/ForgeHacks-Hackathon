from unittest.mock import patch

from src.api_client import analyze_problem, check_health


def test_analyze_problem_sends_expected_request():
    fake_response = type(
        "FakeResponse",
        (),
        {
            "status_code": 200,
            "json": lambda self: {
                "problem": "test problem",
                "status": "completed",
                "result": {
                    "title": "Test",
                    "problem": "test problem",
                    "solution": "Test solution",
                    "impact": "Test impact",
                },
            },
        },
    )()

    with patch(
        "src.api_client.requests.post",
        return_value=fake_response,
    ) as mock_post:
        result = analyze_problem("test problem")

    mock_post.assert_called_once()

    assert result["status"] == "completed"


def test_empty_problem_is_rejected():
    try:
        analyze_problem("")
    except ValueError as exc:
        assert str(exc) == "Problem cannot be empty."
    else:
        raise AssertionError("Expected ValueError.")


def test_health_check():
    fake_response = type(
        "FakeResponse",
        (),
        {"ok": True},
    )()

    with patch(
        "src.api_client.requests.get",
        return_value=fake_response,
    ):
        assert check_health() is True
