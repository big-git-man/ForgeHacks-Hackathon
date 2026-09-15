from typing import Any, Literal

from pydantic import BaseModel, Field, Field, Field


class AgentDecision(BaseModel):
    action: Literal["respond", "tool"]
    reasoning: str
    tool_name: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
