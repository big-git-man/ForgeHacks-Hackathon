import streamlit as st

from src.api_client import analyze_problem, check_health


st.set_page_config(
    page_title="ForgeHacks",
    page_icon="??",
    layout="centered",
)

st.title("ForgeHacks")
st.caption("AI prototype environment")

problem = st.text_area(
    "Describe a real-world problem",
    placeholder="Example: Students struggle to find affordable healthy meals near campus.",
    height=160,
)

if st.button("Analyze Problem", type="primary"):
    if not problem.strip():
        st.warning("Please describe a problem first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                result = analyze_problem(problem)

                st.success("Analysis completed.")

                project = result["result"]

                st.subheader(project["title"])
                st.write(project["solution"])

                st.markdown("### Problem")
                st.write(project["problem"])

                st.markdown("### Expected Impact")
                st.write(project["impact"])

            except Exception as exc:
                st.error(str(exc))

with st.sidebar:
    st.subheader("System Status")

    if check_health():
        st.success("API online")
    else:
        st.error("API offline")

    st.caption("Frontend ? FastAPI ? Application Service")
