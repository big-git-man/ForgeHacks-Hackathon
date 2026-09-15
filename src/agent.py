from dataclasses import dataclass
from typing import Any

from src.tool_executor import ToolExecutor


@dataclass
class ToolCall:
    tool_name: str
    arguments: dict[str, Any]


class Agent:
    def __init__(self, tool_executor: ToolExecutor):
        self.tool_executor = tool_executor

    def execute_tool_call(self, tool_call: ToolCall) -> Any:
        return self.tool_executor.execute(
            tool_call.tool_name,
            tool_call.arguments,
        )

    def available_tools(self) -> list[dict[str, str]]:
        return self.tool_executor.describe_tools()
