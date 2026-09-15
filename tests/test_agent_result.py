from src.agent_result import AgentResultInterpreter
from src.agent_schema import AgentDecision


class FakeLLMClient:
    def generate(self, prompt):
        assert "Original problem:" in prompt
        assert "Tool result:" in prompt
        return "The total is $100."


def test_result_interpreter():
    interpreter = AgentResultInterpreter(
        FakeLLMClient()
    )

    decision = AgentDecision(
        action="tool",
        reasoning="Calculation required.",
        tool_name="calculate_total",
        arguments={
            "price": 20,
            "quantity": 5,
        },
    )

    result = interpreter.interpret(
        "Calculate the total.",
        decision,
        100,
    )

    assert result == "The total is $100."
