from src.agent_decision import AgentDecisionProcessor
from src.agent_schema import AgentDecision
from src.tool_catalog import build_default_registry
from src.tool_executor import ToolExecutor


def test_tool_decision_executes_tool():
    processor = AgentDecisionProcessor(
        ToolExecutor(build_default_registry())
    )

    decision = AgentDecision(
        action="tool",
        reasoning="A calculation is required.",
        tool_name="calculate_total",
        arguments={
            "price": 25,
            "quantity": 4,
        },
    )

    result = processor.process(decision)

    assert result == 100


def test_respond_decision_does_not_execute_tool():
    processor = AgentDecisionProcessor(
        ToolExecutor(build_default_registry())
    )

    decision = AgentDecision(
        action="respond",
        reasoning="No external information is required.",
    )

    assert processor.process(decision) is None


def test_tool_action_requires_tool_name():
    processor = AgentDecisionProcessor(
        ToolExecutor(build_default_registry())
    )

    decision = AgentDecision(
        action="tool",
        reasoning="A tool is required.",
    )

    try:
        processor.process(decision)
        assert False
    except ValueError as exc:
        assert "tool name" in str(exc).lower()
