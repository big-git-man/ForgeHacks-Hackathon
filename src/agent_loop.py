from typing import Any

from src.agent_decision import AgentDecisionProcessor
from src.agent_decision_maker import AgentDecisionMaker


class AgentLoop:
    def __init__(
        self,
        decision_maker: AgentDecisionMaker,
        decision_processor: AgentDecisionProcessor,
    ):
        self.decision_maker = decision_maker
        self.decision_processor = decision_processor

    def run(self, problem: str) -> dict[str, Any]:
        decision = self.decision_maker.decide(problem)

        tool_result = self.decision_processor.process(
            decision
        )

        return {
            "decision": decision,
            "tool_result": tool_result,
        }
