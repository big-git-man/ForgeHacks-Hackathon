from src.prompt_manager import (
    TRUSTLENS_SYSTEM_PROMPT,
    build_trustlens_prompt,
    get_analysis_prompt,
)
from src.prompt_safety import is_prompt_safe
from src.schemas import ProjectIdea, TrustLensAnalysis


class AIOrchestrator:
    def __init__(self, llm_client, retriever=None):
        self.llm_client = llm_client
        self.retriever = retriever

    def analyze_message(self, message: str) -> TrustLensAnalysis:
        if not isinstance(message, str):
            raise TypeError("Message must be a string.")

        message = message.strip()

        if not message:
            raise ValueError("Message cannot be empty.")

        if not is_prompt_safe(message):
            raise ValueError("Input failed prompt safety checks.")

        user_prompt = build_trustlens_prompt(message)

        if self.retriever is not None:
            from src.rag import build_retrieval_context

            context = build_retrieval_context(
                self.retriever,
                message,
            )

            user_prompt = (
                f"{user_prompt}\n\n"
                f"Relevant context:\n{context}"
            )

        combined_prompt = (
            f"{TRUSTLENS_SYSTEM_PROMPT}\n\n"
            f"{user_prompt}"
        ).strip()

        return self.llm_client.generate_structured(
            combined_prompt,
            TrustLensAnalysis,
        )

    def analyze_problem(self, problem: str) -> ProjectIdea:
        if not isinstance(problem, str):
            raise TypeError("Problem must be a string.")

        problem = problem.strip()

        if not problem:
            raise ValueError("Problem cannot be empty.")

        if not is_prompt_safe(problem):
            raise ValueError("Input failed prompt safety checks.")

        system_prompt, user_prompt = get_analysis_prompt(problem)

        if self.retriever is not None:
            from src.rag import build_retrieval_context

            context = build_retrieval_context(
                self.retriever,
                problem,
            )

            user_prompt = (
                f"{user_prompt}\n\n"
                f"Relevant context:\n{context}"
            )

        combined_prompt = (
            f"{system_prompt}\n\n"
            f"{user_prompt}"
        ).strip()

        return self.llm_client.generate_structured(
            combined_prompt,
            ProjectIdea,
        )
