from src.agent_schema import AgentDecision
from src.llm_client import LLMClient


def build_result_prompt(
    problem: str,
    decision: AgentDecision,
    tool_result,
) -> str:
    return f"""
You are completing an AI agent task.

Original problem:
{problem}

Your decision:
{decision.model_dump_json()}

Tool result:
{tool_result}

Provide the final useful response to the user.

Do not mention internal implementation details unless necessary.
""".strip()


class AgentResultInterpreter:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def interpret(
        self,
        problem: str,
        decision: AgentDecision,
        tool_result,
    ) -> str:
        prompt = build_result_prompt(
            problem,
            decision,
            tool_result,
        )

        return self.llm_client.generate(prompt)
