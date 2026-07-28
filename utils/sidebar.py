import streamlit as st

def render_sidebar():
    st.sidebar.image(
        "data/images/logo.png",
        use_container_width=True
    )

    st.sidebar.title("QAInsight AI")

    st.sidebar.markdown("---")

    school = st.sidebar.selectbox(
        "School",
        [
            "All",
            "School of Medicine",
            "School of Pharmacy",
            "School of Science and Technology",
            "School of Oral Health Sciences",
            "School of Health Care Sciences"
        ]
    )

    quarter = st.sidebar.selectbox(
        "Reporting Quarter",
        ["Q1", "Q2", "Q3", "Q4"]
    )

    return school, quarter
