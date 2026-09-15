from dataclasses import dataclass
from typing import Any


@dataclass
class BenchmarkCase:
    name: str
    input: str
    expected: Any
