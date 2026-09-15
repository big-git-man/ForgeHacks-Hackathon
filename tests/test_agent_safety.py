import pytest

from src.agent_safety import SafeAgentRunner
from src.agent_schema import AgentDecision


class FakeAgentLoop:
    def __init__(self, action):
        self.action = action

    def run(self, problem):
        return {
            "decision": AgentDecision(
                action=self.action,
                reasoning="Test.",
            ),
            "tool_result": None,
        }


def test_safe_agent_runner():
    runner = SafeAgentRunner(
        FakeAgentLoop("respond"),
        max_tool_calls=3,
    )

    result = runner.run("Test problem")

    assert result["tool_calls"] == 0


def test_invalid_max_tool_calls():
    with pytest.raises(ValueError):
        SafeAgentRunner(
            FakeAgentLoop("respond"),
            max_tool_calls=0,
        )


def test_tool_call_is_counted():
    runner = SafeAgentRunner(
        FakeAgentLoop("tool"),
        max_tool_calls=3,
    )

    result = runner.run("Test problem")

    assert result["tool_calls"] == 1
