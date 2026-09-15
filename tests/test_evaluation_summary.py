from src.evaluation import EvaluationResult
from src.evaluation_summary import summarize_results


def test_evaluation_summary():
    results = [
        EvaluationResult(
            name="one",
            passed=True,
            score=1.0,
            details="Passed",
        ),
        EvaluationResult(
            name="two",
            passed=False,
            score=0.0,
            details="Failed",
        ),
        EvaluationResult(
            name="three",
            passed=True,
            score=1.0,
            details="Passed",
        ),
    ]

    summary = summarize_results(results)

    assert summary.total == 3
    assert summary.passed == 2
    assert summary.failed == 1
    assert summary.average_score == 2 / 3


def test_empty_summary():
    summary = summarize_results([])

    assert summary.total == 0
    assert summary.average_score == 0.0
