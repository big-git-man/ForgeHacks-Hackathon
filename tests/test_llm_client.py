from src.llm_client import LLMClient


class FakeResponse:
    class Choice:
        class Message:
            content = "Success after retries."

        message = Message()

    choices = [Choice()]


class FakeCompletions:
    def __init__(self):
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1

        if self.calls < 3:
            raise RuntimeError("Simulated API failure.")

        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.chat = type("Chat", (), {})()
        self.chat.completions = FakeCompletions()


def test_llm_retries_until_success():
    client = object.__new__(LLMClient)
    client.client = FakeClient()
    client.model = "test-model"
    client.max_retries = 3
    client.retry_delay = 0

    result = client.generate("Test prompt")

    assert result == "Success after retries."
    assert client.client.chat.completions.calls == 3
