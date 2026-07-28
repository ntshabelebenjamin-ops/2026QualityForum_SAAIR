import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_improvement_plans

st.set_page_config(
    page_title="Continuous Quality Improvement",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Continuous Quality Improvement Tracker")

st.caption(
    "Monitor institutional quality issues, improvement plans, implementation, evidence and impact."
)

# ==========================================================
# LOAD DATA
# ==========================================================

plans = load_improvement_plans()

if plans.empty:
    st.warning("No Improvement Plan data available.")
    st.stop()

# ==========================================================
# CLEAN DATA
# ==========================================================

plans["Progress"] = pd.to_numeric(
    plans["Progress"],
    errors="coerce"
)

plans["BeforeScore"] = pd.to_numeric(
    plans["BeforeScore"],
    errors="coerce"
)

plans["CurrentScore"] = pd.to_numeric(
    plans["CurrentScore"],
    errors="coerce"
)

plans["TargetScore"] = pd.to_numeric(
    plans["TargetScore"],
    errors="coerce"
)

plans["Status"] = (
    plans["Status"]
    .astype(str)
    .str.strip()
    .str.title()
)

# ==========================================================
# FILTERS
# ==========================================================

sources = ["All"] + sorted(
    plans["Source"].dropna().unique().tolist()
)

selected_source = st.sidebar.selectbox(
    "Quality Issue Source",
    sources
)

if selected_source != "All":

    plans = plans[
        plans["Source"] == selected_source
    ]

# ==========================================================
# KPI CARDS
# ==========================================================

issues = len(plans)

completed = (
    plans["Status"] == "Completed"
).sum()

in_progress = (
    plans["Status"] == "In Progress"
).sum()

overdue = (
    plans["Status"] == "Overdue"
).sum()

average_progress = round(
    plans["Progress"].mean(),
    1
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Quality Issues",
    issues
)

c2.metric(
    "Completed",
    completed
)

c3.metric(
    "In Progress",
    in_progress
)

c4.metric(
    "Average Progress",
    f"{average_progress}%"
)

st.metric(
    "Overdue Actions",
    overdue
)

st.divider()

# ==========================================================
# STATUS
# ==========================================================

st.subheader("Improvement Plan Status")

status = (
    plans["Status"]
    .value_counts()
    .reset_index()
)

status.columns = [
    "Status",
    "Count"
]

fig = px.pie(
    status,
    names="Status",
    values="Count",
    hole=.55,
    title="Improvement Plans by Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# SOURCES OF QUALITY ISSUES
# ==========================================================

st.subheader("Quality Issues by Source")

source = (
    plans.groupby("Source")
    .size()
    .reset_index(name="Issues")
)

fig2 = px.bar(
    source,
    x="Source",
    y="Issues",
    text_auto=True,
    title="Quality Issue Sources"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# PROGRESS
# ==========================================================

st.subheader("Improvement Progress")

progress = (
    plans.groupby("Owner")["Progress"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    progress,
    x="Owner",
    y="Progress",
    color="Progress",
    text_auto=".1f",
    title="Average Progress by Responsible Office"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================================
# IMPACT
# ==========================================================

st.subheader("Impact Evaluation")

impact = plans[
    [
        "ImprovementID",
        "Issue",
        "BeforeScore",
        "CurrentScore",
        "TargetScore",
        "Impact"
    ]
]

st.dataframe(
    impact,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# IMPROVEMENT REGISTER
# ==========================================================

st.subheader("Institutional Improvement Register")

st.dataframe(
    plans,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# QAINSIGHT AI
# ==========================================================

st.subheader("🤖 QAInsight AI Continuous Improvement Insight")

highest = plans.loc[
    plans["Progress"].idxmax()
]

lowest = plans.loc[
    plans["Progress"].idxmin()
]

st.info(f"""
## Continuous Quality Improvement Summary

QAInsight AI analysed **{issues} institutional improvement plans**.

### Best Performing Improvement

**Issue**

{highest["Issue"]}

Progress

**{highest["Progress"]:.1f}%**

Owner

**{highest["Owner"]}**

---

### Highest Priority Improvement

**Issue**

{lowest["Issue"]}

Current Progress

**{lowest["Progress"]:.1f}%**

Owner

**{lowest["Owner"]}**

---

### Executive Recommendations

• Prioritise overdue improvement plans.

• Monitor recurring issues across faculties.

• Link student feedback directly to improvement initiatives.

• Review evidence before closing actions.

• Measure whether interventions improved quality indicators.

• Report progress quarterly to Senate and Council.

QAInsight AI recommends shifting institutional reporting from compliance monitoring to continuous quality enhancement supported by evidence.
""")

# ==========================================================
# DOWNLOAD
# ==========================================================

st.divider()

csv = plans.to_csv(index=False)

st.download_button(
    "📥 Download Improvement Register",
    csv,
    "Continuous_Quality_Improvement.csv",
    "text/csv"
)
