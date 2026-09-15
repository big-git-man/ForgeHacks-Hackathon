from src.llm_client import LLMClient
from src.prompt_manager import get_analysis_prompt
from src.prompt_safety import is_prompt_safe
from src.rag import build_retrieval_context
from src.retriever import TfidfRetriever
from src.schemas import ProjectIdea


class AIOrchestrator:
    def __init__(
        self,
        llm_client: LLMClient,
        retriever: TfidfRetriever | None = None,
    ):
        self.llm_client = llm_client
        self.retriever = retriever

    def analyze_problem(self, problem: str) -> ProjectIdea:
        if not problem.strip():
            raise ValueError("Problem cannot be empty.")

        if not is_prompt_safe(problem):
            raise ValueError("Input failed prompt safety checks.")

        system_prompt, user_prompt = get_analysis_prompt(problem)

        if self.retriever is not None:
            context = build_retrieval_context(
                self.retriever,
                problem,
            )

            user_prompt = (
                f"{user_prompt}\n\n"
                f"Relevant context:\n{context}"
            )

        combined_prompt = f"""
{system_prompt}

{user_prompt}
""".strip()

        return self.llm_client.generate_structured(
            combined_prompt,
            ProjectIdea,
        )
