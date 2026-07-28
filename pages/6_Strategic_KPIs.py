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

