import os

import streamlit as st

from src.api_client import analyze_problem, check_health


DEMO_MODE = os.getenv(
    "DEMO_MODE",
    "false",
).lower() == "true"


DEMO_RESULT = {
    "problem": "Students struggle to find affordable healthy meals near campus.",
    "status": "completed",
    "result": {
        "title": "Campus Meal Planner",
        "problem": "Students need a simple way to discover affordable healthy meal options near campus.",
        "solution": "An AI-powered assistant that combines student preferences, budget, location, and dietary needs to generate practical meal options.",
        "impact": "Students can make faster food decisions while staying within their budget and preferences.",
    },
}


def render_result(response: dict) -> None:
    project = response["result"]

    st.success("Analysis completed.")

    st.markdown(f"## {project['title']}")

    st.markdown("### Problem")
    st.write(project["problem"])

    st.markdown("### Solution")
    st.write(project["solution"])

    st.markdown("### Expected Impact")
    st.write(project["impact"])


st.set_page_config(
    page_title="ForgeHacks",
    page_icon="??",
    layout="centered",
)

st.title("ForgeHacks")
st.caption("AI for real-world problems")

st.markdown(
    "Describe a real-world problem and let the AI analyze "
    "the problem, solution, and expected impact."
)

problem = st.text_area(
    "What problem are you trying to solve?",
    placeholder=(
        "Example: Students struggle to find affordable "
        "healthy meals near campus."
    ),
    height=160,
)

col1, col2 = st.columns(2)

with col1:
    analyze_clicked = st.button(
        "Analyze Problem",
        type="primary",
        use_container_width=True,
    )

with col2:
    clear_clicked = st.button(
        "Clear",
        use_container_width=True,
    )

if clear_clicked:
    st.rerun()

if analyze_clicked:
    if not problem.strip():
        st.warning("Please describe a problem first.")
    else:
        try:
            with st.spinner("AI is analyzing the problem..."):
                if DEMO_MODE:
                    response = DEMO_RESULT
                else:
                    response = analyze_problem(problem)

            render_result(response)

        except Exception:
            st.error(
                "Something went wrong while processing the request. "
                "Please try again."
            )

with st.sidebar:
    st.subheader("System")

    if DEMO_MODE:
        st.info("Demo mode enabled")
    elif check_health():
        st.success("API online")
    else:
        st.error("API offline")

    st.divider()

    st.caption(
        "Streamlit ? FastAPI ? Application Service ? AI Pipeline"
    )
