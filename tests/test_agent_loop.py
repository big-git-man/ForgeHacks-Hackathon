from src.agent_decision import AgentDecisionProcessor
from src.agent_decision_maker import AgentDecisionMaker
from src.agent_loop import AgentLoop
from src.agent_schema import AgentDecision
from src.tool_catalog import build_default_registry
from src.tool_executor import ToolExecutor


class FakeLLMClient:
    def generate_structured(self, prompt, schema):
        return AgentDecision(
            action="tool",
            reasoning="Calculation required.",
            tool_name="calculate_total",
            arguments={
                "price": 20,
                "quantity": 5,
            },
        )


def test_agent_loop():
    executor = ToolExecutor(
        build_default_registry()
    )

    loop = AgentLoop(
        AgentDecisionMaker(
            FakeLLMClient(),
            executor,
        ),
        AgentDecisionProcessor(executor),
    )

    result = loop.run(
        "Calculate 5 items at 20 each."
    )

    assert result["decision"].action == "tool"
    assert result["tool_result"] == 100
