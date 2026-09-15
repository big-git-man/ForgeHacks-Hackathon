INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard previous instructions",
    "system prompt",
    "reveal your instructions",
]


def check_prompt_safety(text: str) -> list[str]:
    lowered = text.lower()

    return [
        pattern
        for pattern in INJECTION_PATTERNS
        if pattern in lowered
    ]


def is_prompt_safe(text: str) -> bool:
    return not check_prompt_safety(text)
