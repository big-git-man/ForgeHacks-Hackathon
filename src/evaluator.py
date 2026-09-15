from src.evaluation import EvaluationResult


class Evaluator:
    def evaluate_exact_match(
        self,
        name: str,
        actual,
        expected,
    ) -> EvaluationResult:
        passed = actual == expected

        return EvaluationResult(
            name=name,
            passed=passed,
            score=1.0 if passed else 0.0,
            details=(
                "Output matched expected result."
                if passed
                else f"Expected {expected!r}, got {actual!r}."
            ),
        )
