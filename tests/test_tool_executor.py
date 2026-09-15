from src.tool_catalog import build_default_registry
from src.tool_executor import ToolExecutor


def test_tool_executor():
    executor = ToolExecutor(
        build_default_registry()
    )

    result = executor.execute(
        "calculate_total",
        {
            "price": 20,
            "quantity": 5,
        },
    )

    assert result == 100


def test_tool_descriptions():
    executor = ToolExecutor(
        build_default_registry()
    )

    tools = executor.describe_tools()

    assert len(tools) == 1
    assert tools[0]["name"] == "calculate_total"
    assert tools[0]["description"]


def test_empty_tool_name_is_rejected():
    executor = ToolExecutor(
        build_default_registry()
    )

    try:
        executor.execute("", {})
        assert False
    except ValueError as exc:
        assert "empty" in str(exc).lower()


def test_invalid_arguments_are_rejected():
    executor = ToolExecutor(
        build_default_registry()
    )

    try:
        executor.execute(
            "calculate_total",
            ["invalid"],
        )
        assert False
    except TypeError as exc:
        assert "dictionary" in str(exc).lower()
