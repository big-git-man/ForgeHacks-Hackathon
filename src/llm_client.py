import time

from openai import OpenAI

from src.config import settings


class LLMClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.api_key = api_key or settings.featherless_api_key
        self.base_url = base_url or settings.llm_base_url
        self.model = model or settings.llm_model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        if not self.api_key:
            raise ValueError("API key not configured.")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def generate(self, prompt: str) -> str:
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                )

                return response.choices[0].message.content or ""

            except Exception as exc:
                last_error = exc

                if attempt == self.max_retries:
                    break

                time.sleep(self.retry_delay)

        raise RuntimeError(
            f"LLM request failed after {self.max_retries + 1} attempts."
        ) from last_error

    def generate_json(self, prompt: str) -> str:
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Return only valid JSON. Do not include markdown or additional text.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                )

                return response.choices[0].message.content or "{}"

            except Exception as exc:
                last_error = exc

                if attempt == self.max_retries:
                    break

                time.sleep(self.retry_delay)

        raise RuntimeError(
            f"JSON LLM request failed after {self.max_retries + 1} attempts."
        ) from last_error

    def generate_structured(self, prompt: str, schema):
        raw_output = self.generate_json(prompt)

        try:
            return schema.model_validate_json(raw_output)
        except Exception as exc:
            raise ValueError(
                f"LLM output does not match schema: {schema.__name__}"
            ) from exc
