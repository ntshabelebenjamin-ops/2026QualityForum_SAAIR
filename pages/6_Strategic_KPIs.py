import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_kpis,
    load_app,
    load_risks,
    load_actions
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Strategic KPIs",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Strategic KPIs")
st.caption(
    "Institutional strategic performance, annual performance plan and enterprise risk"
)

# ==========================================================
# LOAD DATA
# ==========================================================

kpis = load_kpis()
app = load_app()
risks = load_risks()
actions = load_actions()

# ==========================================================
# CHECK DATA
# ==========================================================

if kpis.empty:
    st.warning("No Strategic KPI data available.")
    st.stop()

# ==========================================================
# CLEAN DATA
# ==========================================================

for df, column in [
    (kpis, "Status"),
    (actions, "Status"),
    (risks, "RiskLevel")
]:
    if column in df.columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.title()
        )

# ==========================================================
# SIDEBAR FILTER
# ==========================================================

objectives = ["All"] + sorted(
    kpis["StrategicObjective"].dropna().unique().tolist()
)

selected_objective = st.sidebar.selectbox(
    "Strategic Objective",
    objectives
)

if selected_objective != "All":
    kpis = kpis[
        kpis["StrategicObjective"] == selected_objective
    ]

if kpis.empty:
    st.warning("No KPI records found for the selected objective.")
    st.stop()

# ==========================================================
# KPI SUMMARY
# ==========================================================

overall = round(
    kpis["PerformancePercent"].mean(),
    1
)

total_kpis = len(kpis)

achieved = (
    kpis["Status"]
    .str.contains("Achieved", case=False, na=False)
).sum()

on_track = (
    kpis["Status"]
    .str.contains("On Track", case=False, na=False)
).sum()

at_risk = (
    kpis["Status"]
    .str.contains("At Risk", case=False, na=False)
).sum()

overdue = (
    actions["Status"]
    .str.contains("Overdue", case=False, na=False)
).sum()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Overall Performance", f"{overall}%")
c2.metric("Total KPIs", total_kpis)
c3.metric("Achieved", achieved)
c4.metric("On Track", on_track)
c5.metric("At Risk", at_risk)

st.metric("Overdue Actions", overdue)

st.divider()

# ==========================================================
# PERFORMANCE BY STRATEGIC OBJECTIVE
# ==========================================================

st.subheader("Performance by Strategic Objective")

objective_perf = (
    kpis.groupby("StrategicObjective")["PerformancePercent"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    objective_perf,
    x="StrategicObjective",
    y="PerformancePercent",
    color="PerformancePercent",
    text_auto=".1f",
    title="Average Performance by Strategic Objective"
)

st.plotly_chart(fig1, use_container_width=True)

# ==========================================================
# KPI STATUS
# ==========================================================

st.subheader("Strategic KPI Status")

status_df = (
    kpis["Status"]
    .value_counts()
    .reset_index()
)

status_df.columns = [
    "Status",
    "Count"
]

fig2 = px.pie(
    status_df,
    values="Count",
    names="Status",
    hole=0.55,
    title="KPI Status Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================================================
# RISK MATRIX
# ==========================================================

if not risks.empty:

    st.subheader("Enterprise Risk Matrix")

    fig3 = px.scatter(
        risks,
        x="Likelihood",
        y="Impact",
        size="RiskScore",
        color="RiskLevel",
        hover_name="RiskDescription",
        title="Institutional Risk Matrix"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ==========================================================
# HIGH RISKS
# ==========================================================

st.subheader("High Institutional Risks")

high = risks[
    risks["RiskLevel"] == "High"
]

if high.empty:
    st.success("No High Risks Recorded")
else:
    st.dataframe(
        high,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# OUTSTANDING ACTIONS
# ==========================================================

st.subheader("Outstanding Actions")

pending = actions[
    actions["Status"] != "Completed"
]

if pending.empty:
    st.success("No Outstanding Actions")
else:
    st.dataframe(
        pending,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# ANNUAL PERFORMANCE PLAN
# ==========================================================

st.subheader("Annual Performance Plan")

st.dataframe(
    app,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# AI EXECUTIVE SUMMARY
# ==========================================================

st.subheader("🤖 QAInsight AI Executive Summary")

lowest = kpis.loc[
    kpis["PerformancePercent"].idxmin()
]

st.info(f"""
### Executive Summary

Overall institutional performance is **{overall}%** across **{total_kpis} KPIs**.

### Priority KPI

**Strategic Objective:** {lowest['StrategicObjective']}

**KPI:** {lowest['KPI']}

Performance: **{lowest['PerformancePercent']}%**

### Recommended Executive Actions

• Prioritise KPIs below target.

• Monitor enterprise risks monthly.

• Close overdue institutional actions.

• Align improvement plans with strategic objectives.

• Continue evidence-based monitoring through QAInsight AI.
""")

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

st.divider()

csv = kpis.to_csv(index=False)

st.download_button(
    label="📥 Download Strategic KPI Report",
    data=csv,
    file_name="Strategic_KPI_Report.csv",
    mime="text/csv"
)

# ==========================================================
# CREATE KPI STATUS FROM PERFORMANCE
# ==========================================================

def classify_status(score):
    if pd.isna(score):
        return "Unknown"
    elif score >= 90:
        return "Achieved"
    elif score >= 75:
        return "On Track"
    else:
        return "At Risk"

# Create/overwrite Status based on PerformancePercent
kpis["Status"] = kpis["PerformancePercent"].apply(classify_status)

# ==========================================================
# KPI SUMMARY
# ==========================================================

overall = round(
    kpis["PerformancePercent"].mean(),
    1
)

total_kpis = len(kpis)

achieved = (
    kpis["Status"] == "Achieved"
).sum()

on_track = (
    kpis["Status"] == "On Track"
).sum()

at_risk = (
    kpis["Status"] == "At Risk"
).sum()

# ==========================================================
# OVERDUE ACTIONS
# ==========================================================

# If DueDate exists, calculate overdue automatically
if "DueDate" in actions.columns:

    actions["DueDate"] = pd.to_datetime(
        actions["DueDate"],
        errors="coerce"
    )

    overdue = (
        (actions["DueDate"] < pd.Timestamp.today()) &
        (actions["Status"].str.lower() != "completed")
    ).sum()

else:

    overdue = (
        actions["Status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("overdue")
        .sum()
    )

# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Overall Performance",
    f"{overall}%"
)

c2.metric(
    "Total KPIs",
    total_kpis
)

c3.metric(
    "Achieved",
    achieved
)

c4.metric(
    "On Track",
    on_track
)

c5.metric(
    "At Risk",
    at_risk
)

st.metric(
    "Overdue Actions",
    overdue
)
