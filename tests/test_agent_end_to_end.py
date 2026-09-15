from src.agent_decision import AgentDecisionProcessor
from src.agent_decision_maker import AgentDecisionMaker
from src.agent_loop import AgentLoop
from src.agent_result import AgentResultInterpreter
from src.agent_safety import SafeAgentRunner
from src.agent_schema import AgentDecision
from src.tool_catalog import build_default_registry
from src.tool_executor import ToolExecutor


class FakeLLMClient:
    def generate_structured(self, prompt, schema):
        return AgentDecision(
            action="tool",
            reasoning="The total must be calculated.",
            tool_name="calculate_total",
            arguments={
                "price": 25,
                "quantity": 4,
            },
        )

    def generate(self, prompt):
        return "The total is 100."


def test_complete_agent_architecture():
    client = FakeLLMClient()

    executor = ToolExecutor(
        build_default_registry()
    )

    decision_maker = AgentDecisionMaker(
        client,
        executor,
    )

    decision_processor = AgentDecisionProcessor(
        executor
    )

    loop = AgentLoop(
        decision_maker,
        decision_processor,
    )

    runner = SafeAgentRunner(
        loop,
        max_tool_calls=3,
    )

    result = runner.run(
        "What is 25 multiplied by 4?"
    )

    assert result["decision"].action == "tool"
    assert result["decision"].tool_name == "calculate_total"
    assert result["tool_result"] == 100
    assert result["tool_calls"] == 1

    interpreter = AgentResultInterpreter(client)

    final_response = interpreter.interpret(
        "What is 25 multiplied by 4?",
        result["decision"],
        result["tool_result"],
    )

    assert final_response == "The total is 100."
