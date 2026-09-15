import os

import requests


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


def analyze_problem(problem: str) -> dict:
    if not problem.strip():
        raise ValueError("Problem cannot be empty.")

    response = requests.post(
        f"{API_BASE_URL}/analyze",
        json={"problem": problem},
        timeout=60,
    )

    if response.status_code >= 400:
        try:
            detail = response.json().get(
                "detail",
                "API request failed.",
            )
        except ValueError:
            detail = "API request failed."

        raise RuntimeError(str(detail))

    return response.json()


def check_health() -> bool:
    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5,
        )
        return response.ok
    except requests.RequestException:
        return False
