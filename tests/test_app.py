import ast
from pathlib import Path


def test_streamlit_app_exists():
    path = Path("app/main.py")

    assert path.exists()


def test_streamlit_app_compiles():
    path = Path("app/main.py")

    source = path.read_text(encoding="utf-8")

    ast.parse(source)


def test_demo_result_exists():
    source = Path("app/main.py").read_text(
        encoding="utf-8"
    )

    assert "DEMO_RESULT" in source
    assert "DEMO_MODE" in source
