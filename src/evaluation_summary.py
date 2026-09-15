from dataclasses import dataclass

from src.evaluation import EvaluationResult


@dataclass
class EvaluationSummary:
    total: int
    passed: int
    failed: int
    average_score: float


def summarize_results(
    results: list[EvaluationResult],
) -> EvaluationSummary:
    if not results:
        return EvaluationSummary(
            total=0,
            passed=0,
            failed=0,
            average_score=0.0,
        )

    passed = sum(
        result.passed
        for result in results
    )

    average_score = sum(
        result.score
        for result in results
    ) / len(results)

    return EvaluationSummary(
        total=len(results),
        passed=passed,
        failed=len(results) - passed,
        average_score=average_score,
    )
