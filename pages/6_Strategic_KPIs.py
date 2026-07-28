import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_kpis,
    load_app,
    load_risks,
    load_actions
)

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

if kpis.empty:
    st.warning("No Strategic KPI data available.")
    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

objectives = ["All"] + sorted(
    kpis["StrategicObjective"].dropna().unique().tolist()
)

selected = st.sidebar.selectbox(
    "Strategic Objective",
    objectives
)

if selected != "All":
    kpis = kpis[
        kpis["StrategicObjective"] == selected
    ]

# ==========================================================
# KPI SUMMARY
# ==========================================================

overall = round(
    kpis["PerformancePercent"].mean(),
    1
)

achieved = (
    kpis["Status"] == "Achieved"
).sum()

at_risk = (
    kpis["Status"] == "At Risk"
).sum()

overdue = (
    actions["Status"] == "Overdue"
).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Overall Performance",
    f"{overall}%"
)

c2.metric(
    "KPIs Achieved",
    achieved
)

c3.metric(
    "KPIs At Risk",
    at_risk
)

c4.metric(
    "Overdue Actions",
    overdue
)

st.divider()

# ==========================================================
# PERFORMANCE BY STRATEGIC OBJECTIVE
# ==========================================================

st.subheader("Performance by Strategic Objective")

objective = (
    kpis
    .groupby("StrategicObjective")["PerformancePercent"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    objective,
    x="StrategicObjective",
    y="PerformancePercent",
    color="PerformancePercent",
    text_auto=".1f",
    title="Average Performance by Strategic Objective"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================================
# KPI STATUS
# ==========================================================

st.subheader("KPI Status")

status = (
    kpis["Status"]
    .value_counts()
    .reset_index()
)

status.columns = [
    "Status",
    "Count"
]

fig2 = px.pie(
    status,
    values="Count",
    names="Status",
    hole=0.55,
    title="Strategic KPI Status"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# ENTERPRISE RISK
# ==========================================================

st.subheader("Enterprise Risk Register")

fig3 = px.scatter(
    risks,
    x="Likelihood",
    y="Impact",
    size="RiskScore",
    color="RiskLevel",
    hover_name="RiskDescription",
    title="Institutional Risk Matrix"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================================
# RISK REGISTER
# ==========================================================

st.subheader("High Risk Register")

high = risks[
    risks["RiskLevel"] == "High"
]

if high.empty:
    st.success("No high risks recorded.")
else:
    st.dataframe(
        high,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# ACTION TRACKER
# ==========================================================

st.subheader("Outstanding Actions")

pending = actions[
    actions["Status"] != "Completed"
]

st.dataframe(
    pending,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# APP PERFORMANCE
# ==========================================================

st.subheader("Annual Performance Plan")

st.dataframe(
    app,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# AI EXECUTIVE BRIEF
# ==========================================================

st.subheader("🤖 Executive Brief")

priority = kpis.loc[
    kpis["PerformancePercent"].idxmin()
]

st.info(f"""
### Institutional Summary

Overall institutional performance is **{overall}%**.

### Priority KPI

**Strategic Objective:** {priority['StrategicObjective']}

**KPI:** {priority['KPI']}

Performance achieved:

**{priority['PerformancePercent']}%**

### Executive Recommendations

• Prioritise underperforming strategic objectives.

• Accelerate overdue institutional actions.

• Monitor high enterprise risks monthly.

• Review KPIs below target with responsible offices.

• Align improvement plans with institutional strategy.

• Escalate unresolved risks to Executive Management.
""")

# ==========================================================
# DOWNLOAD
# ==========================================================

st.divider()

csv = kpis.to_csv(index=False)

st.download_button(
    "📥 Download Strategic KPI Report",
    csv,
    "Strategic_KPI_Report.csv",
    "text/csv"
)
