from src.benchmark import BenchmarkCase
from src.evaluator import Evaluator


class BenchmarkRunner:
    def __init__(self, evaluator: Evaluator):
        self.evaluator = evaluator

    def run(
        self,
        cases: list[BenchmarkCase],
        executor,
    ):
        results = []

        for case in cases:
            actual = executor(case.input)

            results.append(
                self.evaluator.evaluate_exact_match(
                    case.name,
                    actual,
                    case.expected,
                )
            )

        return results
