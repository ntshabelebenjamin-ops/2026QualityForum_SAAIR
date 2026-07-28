import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_modules,
    load_programme_reviews,
    load_curriculum
)

st.set_page_config(
    page_title="Teaching & Learning",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Teaching & Learning")

st.caption(
    "Monitoring curriculum quality, module performance and programme reviews"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

modules = load_modules()
reviews = load_programme_reviews()
curriculum = load_curriculum()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

schools = ["All"] + sorted(modules["School"].unique().tolist())

selected_school = st.sidebar.selectbox(
    "School",
    schools
)

filtered_modules = modules.copy()

if selected_school != "All":
    filtered_modules = filtered_modules[
        filtered_modules["School"] == selected_school
    ]

# -------------------------------------------------
# KPIs
# -------------------------------------------------

total_modules = len(filtered_modules)

average_pass = round(
    filtered_modules["PassRate"].mean(),
    1
)

under_review = len(
    filtered_modules[
        filtered_modules["ReviewStatus"] == "Under Review"
    ]
)

low_pass = len(
    filtered_modules[
        filtered_modules["PassRate"] < 70
    ]
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Modules", total_modules)
c2.metric("Average Pass Rate", f"{average_pass}%")
c3.metric("Under Review", under_review)
c4.metric("Pass Rate <70%", low_pass)

st.divider()

# -------------------------------------------------
# PASS RATE BY SCHOOL
# -------------------------------------------------

school_pass = (
    filtered_modules
    .groupby("School")["PassRate"]
    .mean()
    .reset_index()
)

fig = px.bar(
    school_pass,
    x="School",
    y="PassRate",
    title="Average Pass Rate by School",
    text_auto=".1f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# ASSESSMENT METHODS
# -------------------------------------------------

assessment = (
    filtered_modules["AssessmentMethod"]
    .value_counts()
    .reset_index()
)

assessment.columns = [
    "Assessment Method",
    "Modules"
]

fig2 = px.pie(
    assessment,
    values="Modules",
    names="Assessment Method",
    hole=0.5,
    title="Assessment Methods"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -------------------------------------------------
# LOW PERFORMING MODULES
# -------------------------------------------------

st.subheader("⚠ Modules Requiring Attention")

attention = filtered_modules[
    filtered_modules["PassRate"] < 70
]

st.dataframe(
    attention,
    use_container_width=True
)

# -------------------------------------------------
# PROGRAMME REVIEWS
# -------------------------------------------------

st.subheader("Programme Reviews")

st.dataframe(
    reviews,
    use_container_width=True
)

# -------------------------------------------------
# CURRICULUM MAPPING
# -------------------------------------------------

st.subheader("Curriculum Mapping")

st.dataframe(
    curriculum,
    use_container_width=True
)

# -------------------------------------------------
# AI INSIGHT
# -------------------------------------------------

st.subheader("🤖 AI Teaching Insight")

if low_pass == 0:

    st.success(
        """
All modules currently exceed the institutional
minimum pass rate threshold.
Continue monitoring assessment quality and
curriculum relevance.
"""
    )

else:

    st.warning(
        f"""
There are **{low_pass} module(s)** with a pass
rate below 70%.

Consider reviewing:

• Assessment strategies

• Student support interventions

• Curriculum alignment

• Teaching approaches

These modules should be prioritised during the
next programme review cycle.
"""
    )

st.divider()

csv = filtered_modules.to_csv(index=False)

st.download_button(
    "📥 Download Teaching Report",
    csv,
    "Teaching_Learning_Report.csv",
    "text/csv"
)
