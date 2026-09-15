import time
from typing import Any

from src.logger import get_logger
from src.metrics import metrics
from src.tools import ToolRegistry


logger = get_logger("tool_executor")


class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        if not tool_name.strip():
            raise ValueError(
                "Tool name cannot be empty."
            )

        if not isinstance(arguments, dict):
            raise TypeError(
                "Tool arguments must be a dictionary."
            )

        metrics.tools.total_calls += 1
        start_time = time.perf_counter()

        logger.info(
            f"TOOL START | name={tool_name}"
        )

        try:
            result = self.registry.execute(
                tool_name,
                **arguments,
            )

            metrics.tools.successful_calls += 1

            logger.info(
                f"TOOL END | name={tool_name}"
            )

            return result

        except Exception:
            metrics.tools.failed_calls += 1

            logger.exception(
                f"TOOL ERROR | name={tool_name}"
            )

            raise

        finally:
            metrics.tools.total_latency_ms += (
                time.perf_counter() - start_time
            ) * 1000

    def describe_tools(self) -> list[dict[str, str]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in self.registry.list_tools()
        ]
