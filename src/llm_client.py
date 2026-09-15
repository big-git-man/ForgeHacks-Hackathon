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
        timeout: float = 30.0,
    ):
        self.api_key = api_key or settings.featherless_api_key
        self.base_url = base_url or settings.llm_base_url
        self.model = model or settings.llm_model
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("API key not configured.")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

    def _request(self, prompt: str, json_mode: bool = False) -> str:
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                kwargs = {
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                }

                if json_mode:
                    kwargs["messages"] = [
                        {
                            "role": "system",
                            "content": (
                                "Return only valid JSON. "
                                "Do not include markdown or additional text."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ]
                    kwargs["response_format"] = {"type": "json_object"}

                response = self.client.chat.completions.create(**kwargs)

                return response.choices[0].message.content or ""

            except Exception as exc:
                last_error = exc

                if attempt == self.max_retries:
                    break

                delay = self.retry_delay * (2 ** attempt)
                time.sleep(delay)

        raise RuntimeError(
            f"LLM request failed after {self.max_retries + 1} attempts."
        ) from last_error

    def generate(self, prompt: str) -> str:
        return self._request(prompt, json_mode=False)

    def generate_json(self, prompt: str) -> str:
        return self._request(prompt, json_mode=True)

    def generate_structured(self, prompt: str, schema):
        raw_output = self.generate_json(prompt)

        try:
            return schema.model_validate_json(raw_output)
        except Exception as exc:
            raise ValueError(
                f"LLM output does not match schema: {schema.__name__}"
            ) from exc
