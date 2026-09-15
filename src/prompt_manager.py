from src.prompt_templates import GENERAL_ANALYSIS


PROMPT_VERSION = "v1.0"


def get_analysis_prompt(problem: str) -> tuple[str, str]:
    return GENERAL_ANALYSIS.build(problem=problem)


def get_prompt_version() -> str:
    return PROMPT_VERSION
