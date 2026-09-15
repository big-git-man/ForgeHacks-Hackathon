from typing import Any

from src.tools import ToolRegistry


class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        if not tool_name.strip():
            raise ValueError("Tool name cannot be empty.")

        if not isinstance(arguments, dict):
            raise TypeError("Tool arguments must be a dictionary.")

        return self.registry.execute(
            tool_name,
            **arguments,
        )

    def describe_tools(self) -> list[dict[str, str]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in self.registry.list_tools()
        ]
