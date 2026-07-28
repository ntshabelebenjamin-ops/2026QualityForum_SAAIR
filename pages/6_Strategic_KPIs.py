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
# CLEAN PERFORMANCE DATA
# ==========================================================

kpis["PerformancePercent"] = pd.to_numeric(
    kpis["PerformancePercent"],
    errors="coerce"
)

# ==========================================================
# CREATE KPI STATUS
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

kpis["Status"] = (
    kpis["PerformancePercent"]
    .apply(classify_status)
)

# ==========================================================
# CLEAN DATA
# ==========================================================

for df, column in [
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
    kpis["StrategicObjective"]
    .dropna()
    .unique()
    .tolist()
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
    st.warning("No KPI records found.")
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

if "DueDate" in actions.columns:

    actions["DueDate"] = pd.to_datetime(
        actions["DueDate"],
        errors="coerce"
    )

    overdue = (
        (
            actions["DueDate"] <
            pd.Timestamp.today()
        )
        &
        (
            actions["Status"]
            .astype(str)
            .str.lower()
            .str.strip()
            != "completed"
        )
    ).sum()

else:

    overdue = (
        actions["Status"]
        .astype(str)
        .str.lower()
        .str.strip()
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

st.divider()

# ==========================================================
# PERFORMANCE BY STRATEGIC OBJECTIVE
# ==========================================================

st.subheader("📊 Performance by Strategic Objective")

objective_perf = (
    kpis.groupby("StrategicObjective", as_index=False)
    ["PerformancePercent"]
    .mean()
)

objective_perf = objective_perf.sort_values(
    by="PerformancePercent",
    ascending=False
)

fig1 = px.bar(
    objective_perf,
    x="StrategicObjective",
    y="PerformancePercent",
    color="PerformancePercent",
    text_auto=".1f",
    title="Average Performance by Strategic Objective"
)

fig1.update_layout(
    xaxis_title="Strategic Objective",
    yaxis_title="Average Performance (%)",
    coloraxis_showscale=False
)

fig1.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================================
# KPI STATUS DISTRIBUTION
# ==========================================================

st.subheader("🎯 Strategic KPI Status")

status_df = (
    kpis["Status"]
    .fillna("Unknown")
    .value_counts()
    .rename_axis("Status")
    .reset_index(name="Count")
)

fig2 = px.pie(
    status_df,
    names="Status",
    values="Count",
    hole=0.55,
    title="Strategic KPI Status Distribution"
)

fig2.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# ENTERPRISE RISK MATRIX
# ==========================================================

if not risks.empty:

    st.subheader("⚠️ Enterprise Risk Matrix")

    # Convert numeric columns
    for col in ["Likelihood", "Impact", "RiskScore"]:
        if col in risks.columns:
            risks[col] = pd.to_numeric(
                risks[col],
                errors="coerce"
            )

    fig3 = px.scatter(
        risks,
        x="Likelihood",
        y="Impact",
        size="RiskScore",
        color="RiskLevel",
        hover_name="RiskDescription",
        hover_data=["RiskOwner"],
        title="Institutional Risk Matrix"
    )

    fig3.update_layout(
        xaxis_title="Likelihood",
        yaxis_title="Impact"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

else:

    st.info("No institutional risk data available.")


# ==========================================================
# HIGH INSTITUTIONAL RISKS
# ==========================================================

st.subheader("🚨 High Institutional Risks")

if not risks.empty:

    high = risks[
        risks["RiskLevel"]
        .astype(str)
        .str.upper()
        .eq("HIGH")
    ]

    if high.empty:

        st.success(
            "No High Risks Recorded"
        )

    else:

        st.dataframe(
            high.sort_values(
                "RiskScore",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

else:

    st.info("No risk register available.")

# ==========================================================
# OUTSTANDING ACTIONS
# ==========================================================

st.subheader("📋 Outstanding Actions")

if not actions.empty:

    pending = actions[
        actions["Status"]
        .astype(str)
        .str.lower()
        .str.strip()
        != "completed"
    ]

    if pending.empty:

        st.success(
            "All institutional actions have been completed."
        )

    else:

        st.dataframe(
            pending,
            use_container_width=True,
            hide_index=True
        )

else:

    st.info("No action tracker available.")

# ==========================================================
# ANNUAL PERFORMANCE PLAN
# ==========================================================

st.subheader("📑 Annual Performance Plan")

if not app.empty:

    st.dataframe(
        app,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Annual Performance Plan data available.")

# ==========================================================
# QAINSIGHT AI EXECUTIVE SUMMARY
# ==========================================================

st.subheader("🤖 QAInsight AI Executive Summary")

lowest = kpis.loc[
    kpis["PerformancePercent"].idxmin()
]

highest = kpis.loc[
    kpis["PerformancePercent"].idxmax()
]

st.info(f"""
## Institutional Performance Summary

QAInsight AI analysed **{total_kpis} Strategic KPIs**.

### Overall Institutional Performance

**{overall}%**

---

### Best Performing KPI

**Strategic Objective:** {highest['StrategicObjective']}

**KPI:** {highest['KPI']}

Performance: **{highest['PerformancePercent']:.1f}%**

---

### Lowest Performing KPI

**Strategic Objective:** {lowest['StrategicObjective']}

**KPI:** {lowest['KPI']}

Performance: **{lowest['PerformancePercent']:.1f}%**

---

### KPI Distribution

✅ Achieved: **{achieved}**

🟡 On Track: **{on_track}**

🔴 At Risk: **{at_risk}**

---

### Recommended Executive Actions

• Prioritise KPIs performing below 75%.

• Monitor strategic risks through monthly Executive Management Committee meetings.

• Accelerate implementation of overdue institutional actions.

• Strengthen evidence collection for Annual Performance Plan reporting.

• Review improvement plans for underperforming strategic objectives.

• Continue using QAInsight AI to support evidence-based institutional decision making.
""")
