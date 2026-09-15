from src.llm_client import LLMClient
from src.schemas import ProjectIdea


class FakeResponse:
    class Choice:
        class Message:
            content = """
            {
                "title": "Test AI Project",
                "problem": "A real-world problem",
                "solution": "A practical AI solution",
                "impact": "Positive real-world impact"
            }
            """

        message = Message()

    choices = [Choice()]


class FakeCompletions:
    def create(self, **kwargs):
        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.chat = type("Chat", (), {})()
        self.chat.completions = FakeCompletions()


def test_generate_structured():
    client = object.__new__(LLMClient)
    client.client = FakeClient()
    client.model = "test-model"
    client.max_retries = 0
    client.retry_delay = 0

    result = client.generate_structured(
        "Create a project idea.",
        ProjectIdea,
    )

    assert isinstance(result, ProjectIdea)
    assert result.title == "Test AI Project"
    assert result.problem == "A real-world problem"
    assert result.solution == "A practical AI solution"
    assert result.impact == "Positive real-world impact"
