from src.agent_schema import AgentDecision
from src.agent_prompts import build_agent_decision_prompt
from src.tool_executor import ToolExecutor
from src.llm_client import LLMClient


class AgentDecisionMaker:
    def __init__(
        self,
        llm_client: LLMClient,
        tool_executor: ToolExecutor,
    ):
        self.llm_client = llm_client
        self.tool_executor = tool_executor

    def decide(self, problem: str) -> AgentDecision:
        if not problem.strip():
            raise ValueError("Problem cannot be empty.")

        prompt = build_agent_decision_prompt(
            problem,
            self.tool_executor,
        )

        return self.llm_client.generate_structured(
            prompt,
            AgentDecision,
        )
