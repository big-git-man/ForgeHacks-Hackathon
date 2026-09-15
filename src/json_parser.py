import json

from pydantic import ValidationError

from src.schemas import ProjectIdea


def parse_project_idea(raw_output: str) -> ProjectIdea:
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM output is not valid JSON.") from exc

    try:
        return ProjectIdea.model_validate(data)
    except ValidationError as exc:
        raise ValueError("LLM output does not match the expected project schema.") from exc
