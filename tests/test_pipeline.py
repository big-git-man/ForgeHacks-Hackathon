from src.pipeline import prepare_prompt, validate_project_idea


def test_prepare_prompt():
    system_prompt, user_prompt = prepare_prompt("Test problem")

    assert system_prompt
    assert user_prompt
    assert "Test problem" in user_prompt


def test_validate_project_idea():
    data = {
        "title": "Test Project",
        "problem": "Test problem",
        "solution": "Test solution",
        "impact": "Test impact",
    }

    result = validate_project_idea(data)

    assert result.title == "Test Project"
    assert result.problem == "Test problem"
    assert result.solution == "Test solution"
    assert result.impact == "Test impact"