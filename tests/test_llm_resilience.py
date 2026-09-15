from src.llm_client import LLMClient


class FakeResponse:
    class Choice:
        class Message:
            content = "Success."

        message = Message()

    choices = [Choice()]


class FakeCompletions:
    def __init__(self):
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1

        assert kwargs["model"] == "test-model"

        if self.calls < 3:
            raise RuntimeError("Temporary failure.")

        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.chat = type("Chat", (), {})()
        self.chat.completions = FakeCompletions()


def test_exponential_retry():
    client = object.__new__(LLMClient)

    client.client = FakeClient()
    client.model = "test-model"
    client.max_retries = 3
    client.retry_delay = 0
    client.timeout = 30

    result = client.generate("Test prompt")

    assert result == "Success."
    assert client.client.chat.completions.calls == 3


def test_timeout_configuration():
    client = object.__new__(LLMClient)

    client.model = "test-model"
    client.max_retries = 3
    client.retry_delay = 1
    client.timeout = 45

    assert client.timeout == 45
