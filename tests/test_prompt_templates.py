from src.prompt_templates import build_analysis_prompt


def test_build_analysis_prompt():
    system_prompt, user_prompt = build_analysis_prompt(
        "Students struggle to find affordable study resources."
    )

    assert system_prompt
    assert user_prompt
    assert "Students struggle" in user_prompt


def test_prompt_does_not_leave_template_variables():
    _, user_prompt = build_analysis_prompt("Test problem")

    assert "{problem}" not in user_prompt
