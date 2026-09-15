from src.evaluator import Evaluator


def test_exact_match_passes():
    evaluator = Evaluator()

    result = evaluator.evaluate_exact_match(
        "test_case",
        10,
        10,
    )

    assert result.passed is True
    assert result.score == 1.0
    assert result.name == "test_case"


def test_exact_match_fails():
    evaluator = Evaluator()

    result = evaluator.evaluate_exact_match(
        "test_case",
        10,
        20,
    )

    assert result.passed is False
    assert result.score == 0.0
    assert "Expected 20" in result.details
