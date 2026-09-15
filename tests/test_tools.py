from src.tool_catalog import build_default_registry, calculate_total
from src.tools import Tool, ToolRegistry


def test_calculate_total():
    assert calculate_total(25, 4) == 100


def test_tool_registry():
    registry = ToolRegistry()

    tool = Tool(
        name="test_tool",
        description="A test tool.",
        function=lambda value: value * 2,
    )

    registry.register(tool)

    assert registry.get("test_tool") is tool
    assert registry.execute("test_tool", value=5) == 10


def test_default_registry():
    registry = build_default_registry()

    result = registry.execute(
        "calculate_total",
        price=12.5,
        quantity=4,
    )

    assert result == 50


def test_duplicate_tools_are_rejected():
    registry = ToolRegistry()

    tool = Tool(
        name="duplicate",
        description="Test.",
        function=lambda: True,
    )

    registry.register(tool)

    try:
        registry.register(tool)
        assert False
    except ValueError as exc:
        assert "already registered" in str(exc)
