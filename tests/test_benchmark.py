from src.benchmark import BenchmarkCase
from src.benchmark_runner import BenchmarkRunner
from src.evaluator import Evaluator


def test_benchmark_runner():
    cases = [
        BenchmarkCase(
            name="case_one",
            input="2 + 2",
            expected=4,
        ),
        BenchmarkCase(
            name="case_two",
            input="3 + 3",
            expected=6,
        ),
    ]

    def executor(value):
        if value == "2 + 2":
            return 4

        return 6

    runner = BenchmarkRunner(
        Evaluator()
    )

    results = runner.run(
        cases,
        executor,
    )

    assert len(results) == 2
    assert all(result.passed for result in results)
