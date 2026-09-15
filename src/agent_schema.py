from typing import Any, Literal

from pydantic import BaseModel


class AgentDecision(BaseModel):
    action: Literal["respond", "tool"]
    reasoning: str
    tool_name: str | None = None
    arguments: dict[str, Any] = {}
