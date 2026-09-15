from dataclasses import dataclass


@dataclass
class EvaluationResult:
    name: str
    passed: bool
    score: float
    details: str
