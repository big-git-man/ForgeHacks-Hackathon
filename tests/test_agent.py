from src.agent import Agent, ToolCall
from src.tool_catalog import build_default_registry
from src.tool_executor import ToolExecutor


def test_agent_executes_tool_call():
    executor = ToolExecutor(
        build_default_registry()
    )

    agent = Agent(executor)

    call = ToolCall(
        tool_name="calculate_total",
        arguments={
            "price": 15,
            "quantity": 4,
        },
    )

    result = agent.execute_tool_call(call)

    assert result == 60


def test_agent_exposes_available_tools():
    executor = ToolExecutor(
        build_default_registry()
    )

    agent = Agent(executor)

    tools = agent.available_tools()

    assert len(tools) == 1
    assert tools[0]["name"] == "calculate_total"


def test_tool_call_stores_arguments():
    call = ToolCall(
        tool_name="test",
        arguments={"value": 42},
    )

    assert call.tool_name == "test"
    assert call.arguments["value"] == 42
