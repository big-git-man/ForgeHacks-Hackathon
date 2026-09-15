from src.config import settings


def validate_environment() -> list[str]:
    errors = []

    if not settings.app_env:
        errors.append("APP_ENV is not configured.")

    if not settings.llm_model:
        errors.append("LLM_MODEL is not configured.")

    if not settings.featherless_api_key:
        errors.append("FEATHERLESS_API_KEY is not configured.")

    return errors


if __name__ == "__main__":
    errors = validate_environment()

    if errors:
        print("Environment validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Environment validation passed.")
