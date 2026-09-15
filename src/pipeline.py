from src.prompts import build_system_prompt, build_user_prompt
from src.schemas import ProjectIdea


def prepare_prompt(problem: str) -> tuple[str, str]:
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(problem)

    return system_prompt, user_prompt


def validate_project_idea(data: dict) -> ProjectIdea:
    return ProjectIdea.model_validate(data)