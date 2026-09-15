import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    featherless_api_key: str | None = os.getenv("FEATHERLESS_API_KEY")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")

    app_env: str = os.getenv("APP_ENV", "development")

    llm_model: str = os.getenv(
        "LLM_MODEL",
        "placeholder-model",
    )

    llm_base_url: str | None = os.getenv(
        "LLM_BASE_URL"
    )


settings = Settings()
