from src.tool_executor import ToolExecutor


def build_agent_decision_prompt(
    problem: str,
    tool_executor: ToolExecutor,
) -> str:
    tools = tool_executor.describe_tools()

    tool_descriptions = "\n".join(
        f"- {tool['name']}: {tool['description']}"
        for tool in tools
    )

    return f"""
You are an AI agent solving a practical problem.

Available tools:
{tool_descriptions}

User problem:
{problem}

Decide whether you need a tool.

Return JSON matching this structure:

{{
    "action": "respond" or "tool",
    "reasoning": "brief explanation",
    "tool_name": "tool name or null",
    "arguments": {{}}
}}

Only select a tool when it provides meaningful value.
""".strip()
