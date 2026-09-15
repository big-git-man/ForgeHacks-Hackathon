from src.orchestrator import AIOrchestrator
from src.retriever import Document, TfidfRetriever
from src.schemas import ProjectIdea


class FakeLLMClient:
    def __init__(self):
        self.calls = 0
        self.last_prompt = ""

    def generate_structured(self, prompt, schema):
        self.calls += 1
        self.last_prompt = prompt

        assert schema is ProjectIdea

        return ProjectIdea(
            title="Test Project",
            problem="Test problem",
            solution="Test solution",
            impact="Test impact",
        )


def test_orchestrator_with_retriever():
    retriever = TfidfRetriever()

    retriever.add_documents(
        [
            Document(
                doc_id="health",
                text="Medical imaging can help doctors detect disease.",
                metadata={"category": "health"},
            ),
            Document(
                doc_id="education",
                text="AI tutors can help students learn.",
                metadata={"category": "education"},
            ),
        ]
    )

    client = FakeLLMClient()

    orchestrator = AIOrchestrator(
        client,
        retriever=retriever,
    )

    result = orchestrator.analyze_problem(
        "Doctors need help analyzing medical imaging."
    )

    assert isinstance(result, ProjectIdea)
    assert client.calls == 1
    assert "Relevant context:" in client.last_prompt
    assert "health" in client.last_prompt
