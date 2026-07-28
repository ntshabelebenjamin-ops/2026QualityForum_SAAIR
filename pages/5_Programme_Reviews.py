import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_programme_reviews,
    load_ser,
    load_modules,
    load_quality_standards
)

st.set_page_config(
    page_title="Programme Reviews",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Programme Reviews")

st.caption(
    "Programme quality, accreditation, self-evaluation and continuous improvement"
)

# ==========================================================
# LOAD DATA
# ==========================================================

reviews = load_programme_reviews()
ser = load_ser()
modules = load_modules()
quality = load_quality_standards()

# ==========================================================
# CHECK DATA
# ==========================================================

if reviews.empty:
    st.warning("No programme review data available.")
    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

programmes = ["All"] + sorted(
    reviews["ProgrammeID"].dropna().unique().tolist()
)

selected_programme = st.sidebar.selectbox(
    "Programme",
    programmes
)

if selected_programme != "All":
    reviews = reviews[
        reviews["ProgrammeID"] == selected_programme
    ]

    ser = ser[
        ser["ProgrammeID"] == selected_programme
    ]

    modules = modules[
        modules["ProgrammeID"] == selected_programme
    ]

# ==========================================================
# KPI CARDS
# ==========================================================

total_reviews = len(reviews)

average_score = round(
    reviews["OverallScore"].mean(),
    1
)

under_review = (
    reviews["Status"] == "In Progress"
).sum()

high_risk = (
    ser["RiskLevel"] == "High"
).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Programme Reviews",
    total_reviews
)

c2.metric(
    "Average Score",
    f"{average_score}%"
)

c3.metric(
    "Reviews In Progress",
    under_review
)

c4.metric(
    "High Risk Findings",
    high_risk
)

st.divider()

# ==========================================================
# REVIEW OUTCOMES
# ==========================================================

st.subheader("Programme Review Outcomes")

outcomes = (
    reviews["Outcome"]
    .value_counts()
    .reset_index()
)

outcomes.columns = [
    "Outcome",
    "Programmes"
]

fig1 = px.bar(
    outcomes,
    x="Outcome",
    y="Programmes",
    text_auto=True,
    title="Programme Review Outcomes"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================================
# REVIEW SCORES
# ==========================================================

st.subheader("Programme Review Scores")

fig2 = px.bar(
    reviews.sort_values("OverallScore"),
    x="ProgrammeID",
    y="OverallScore",
    color="OverallScore",
    text_auto=".1f",
    title="Overall Review Scores"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# SER RISK LEVELS
# ==========================================================

st.subheader("SER Risk Distribution")

risk = (
    ser["RiskLevel"]
    .value_counts()
    .reset_index()
)

risk.columns = [
    "Risk Level",
    "Count"
]

fig3 = px.pie(
    risk,
    values="Count",
    names="Risk Level",
    hole=0.55,
    title="Self-Evaluation Report Risk Levels"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================================
# QUALITY STANDARDS
# ==========================================================

st.subheader("Quality Standards")

st.dataframe(
    quality,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# LOW PASS RATE MODULES
# ==========================================================

st.subheader("Modules Requiring Attention")

attention = modules[
    modules["PassRate"] < 70
]

if attention.empty:

    st.success(
        "No modules currently have pass rates below 70%."
    )

else:

    st.dataframe(
        attention[
            [
                "ModuleCode",
                "ModuleName",
                "PassRate",
                "AverageMark",
                "ReviewStatus"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# PROGRAMME REVIEW DETAILS
# ==========================================================

st.subheader("Programme Review Register")

st.dataframe(
    reviews,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# AI QUALITY INSIGHT
# ==========================================================

st.subheader("🤖 QAInsight AI Recommendation")

lowest = reviews.loc[
    reviews["OverallScore"].idxmin()
]

st.info(f"""
### Priority Programme

**Programme:** {lowest['ProgrammeID']}

**Overall Review Score:** {lowest['OverallScore']}%

### Recommended Actions

• Prioritise implementation of outstanding programme review recommendations.

• Review Self-Evaluation Report evidence for compliance gaps.

• Strengthen curriculum alignment with graduate attributes.

• Improve module performance where pass rates are below institutional thresholds.

• Monitor improvement plans through the Action Tracker.

• Schedule a follow-up quality review within the next reporting cycle.
""")

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

st.divider()

csv = reviews.to_csv(index=False)

st.download_button(
    label="📥 Download Programme Review Report",
    data=csv,
    file_name="Programme_Review_Report.csv",
    mime="text/csv"
)
