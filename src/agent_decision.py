from typing import Any

from src.agent_schema import AgentDecision
from src.tool_executor import ToolExecutor


class AgentDecisionProcessor:
    def __init__(self, tool_executor: ToolExecutor):
        self.tool_executor = tool_executor

    def process(self, decision: AgentDecision) -> Any:
        if decision.action == "respond":
            return None

        if not decision.tool_name:
            raise ValueError(
                "Tool action requires a tool name."
            )

        return self.tool_executor.execute(
            decision.tool_name,
            decision.arguments,
        )
