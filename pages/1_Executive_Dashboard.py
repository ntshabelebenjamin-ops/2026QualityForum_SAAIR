import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_kpis,
    load_risks,
    load_actions
)
st.sidebar.header("Filters")

selected_office = st.sidebar.selectbox(
    "Responsible Office",
    ["All"] + sorted(kpis["ResponsibleOffice"].unique().tolist())
)

selected_status = st.sidebar.selectbox(
    "Status",
    ["All"] + sorted(kpis["Status"].unique().tolist())
)

filtered_kpis = kpis.copy()

if selected_office != "All":
    filtered_kpis = filtered_kpis[
        filtered_kpis["ResponsibleOffice"] == selected_office
    ]

if selected_status != "All":
    filtered_kpis = filtered_kpis[
        filtered_kpis["Status"] == selected_status
    ]
from utils.ai_engine import (
    executive_summary,
    high_risk_items,
    overdue_actions
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

st.title("📊 Executive Dashboard")

st.caption(
    "Institutional Performance Overview"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

kpis = load_kpis()
risks = load_risks()
actions = load_actions()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

total_kpis = len(kpis)

on_track = len(
    kpis[
        kpis["Status"].isin(
            ["On Track", "Exceeded Target"]
        )
    ]
)

off_track = len(
    kpis[
        kpis["Status"] == "Off Track"
    ]
)

high_risks = len(
    risks[
        risks["RiskLevel"] == "High"
    ]
)

open_actions = len(
    actions[
        actions["Status"] != "Completed"
    ]
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("KPIs", total_kpis)
c2.metric("On Track", on_track)
c3.metric("Off Track", off_track)
c4.metric("High Risks", high_risks)
c5.metric("Open Actions", open_actions)

st.divider()

# --------------------------------------------------
# Performance by Status
# --------------------------------------------------

status_counts = (
    kpis["Status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Status",
    "Count"
]

fig = px.bar(
    status_counts,
    x="Status",
    y="Count",
    title="Strategic KPI Performance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# High Risk Register
# --------------------------------------------------

st.subheader("⚠ High Risk Register")

st.dataframe(
    high_risk_items(risks),
    use_container_width=True
)

# --------------------------------------------------
# AI Executive Brief
# --------------------------------------------------

st.subheader("🤖 AI Executive Brief")

st.markdown(
    executive_summary(kpis)
)

# --------------------------------------------------
# Outstanding Actions
# --------------------------------------------------

st.subheader("📋 Outstanding Actions")

st.dataframe(
    overdue_actions(actions),
    use_container_width=True
)
