import os
import time

from openai import OpenAI


class LLMClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str = "placeholder-model",
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.api_key = api_key or os.getenv("FEATHERLESS_API_KEY")
        self.base_url = base_url
        self.model = model
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
