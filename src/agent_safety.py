from typing import Any

from src.agent_loop import AgentLoop


class SafeAgentRunner:
    def __init__(
        self,
        agent_loop: AgentLoop,
        max_tool_calls: int = 3,
    ):
        if max_tool_calls < 1:
            raise ValueError(
                "max_tool_calls must be at least 1."
            )

        self.agent_loop = agent_loop
        self.max_tool_calls = max_tool_calls

    def run(self, problem: str) -> dict[str, Any]:
        result = self.agent_loop.run(problem)

        decision = result["decision"]

        if decision.action == "tool":
            result["tool_calls"] = 1
        else:
            result["tool_calls"] = 0

        if result["tool_calls"] > self.max_tool_calls:
            raise RuntimeError(
                "Maximum tool call limit exceeded."
            )

        return result
