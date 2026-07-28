import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_kpis,
    load_risks,
    load_actions
)

from utils.ai_engine import (
    executive_summary,
    high_risk_items,
    overdue_actions
)

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Dashboard")
st.caption("AI-Powered Quality Assurance Decision Support")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

kpis = load_kpis()
risks = load_risks()
actions = load_actions()

# -------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------

st.sidebar.header("Dashboard Filters")

office_list = ["All"] + sorted(
    kpis["ResponsibleOffice"].dropna().unique().tolist()
)

status_list = ["All"] + sorted(
    kpis["Status"].dropna().unique().tolist()
)

selected_office = st.sidebar.selectbox(
    "Responsible Office",
    office_list
)

selected_status = st.sidebar.selectbox(
    "KPI Status",
    status_list
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

# -------------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------------

total_kpis = len(filtered_kpis)

on_track = len(
    filtered_kpis[
        filtered_kpis["Status"].isin(
            ["On Track", "Exceeded Target"]
        )
    ]
)

off_track = len(
    filtered_kpis[
        filtered_kpis["Status"] == "Off Track"
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

health_score = 0

if total_kpis > 0:
    health_score = round(
        (on_track / total_kpis) * 100,
        1
    )

# -------------------------------------------------------
# KPI CARDS
# -------------------------------------------------------

st.subheader("Executive Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Strategic KPIs", total_kpis)

c2.metric(
    "On Track",
    on_track
)

c3.metric(
    "Off Track",
    off_track
)

c4.metric(
    "High Risks",
    high_risks
)

c5.metric(
    "Open Actions",
    open_actions
)

st.divider()

# -------------------------------------------------------
# HEALTH SCORE
# -------------------------------------------------------

st.subheader("Institutional Health")

st.progress(health_score / 100)

st.metric(
    "Health Score",
    f"{health_score}%"
)

st.divider()

# -------------------------------------------------------
# KPI STATUS CHART
# -------------------------------------------------------

status_counts = (
    filtered_kpis["Status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Status",
    "Count"
]

fig = px.pie(
    status_counts,
    values="Count",
    names="Status",
    hole=0.55,
    title="Strategic KPI Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------------
# SEARCH
# -------------------------------------------------------

search = st.text_input(
    "🔍 Search KPI"
)

display_kpis = filtered_kpis.copy()

if search:

    display_kpis = display_kpis[
        display_kpis["KPI"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

# -------------------------------------------------------
# KPI TABLE
# -------------------------------------------------------

st.subheader("Strategic KPIs")

st.dataframe(
    display_kpis,
    use_container_width=True
)

st.divider()

# -------------------------------------------------------
# HIGH RISK REGISTER
# -------------------------------------------------------

st.subheader("⚠ High Risk Register")

st.dataframe(
    high_risk_items(risks),
    use_container_width=True
)

st.divider()

# -------------------------------------------------------
# AI EXECUTIVE SUMMARY
# -------------------------------------------------------

st.subheader("🤖 AI Executive Summary")

st.markdown(
    executive_summary(filtered_kpis)
)

st.divider()

# -------------------------------------------------------
# AI RECOMMENDATIONS
# -------------------------------------------------------

st.subheader("AI Recommendations")

if off_track > 0:

    st.warning(
        f"""
There are **{off_track} strategic KPIs**
currently off track.

Management should prioritise these KPIs,
review improvement plans,
and monitor implementation monthly.
"""
    )

else:

    st.success(
        "All strategic KPIs are currently on track."
    )

st.divider()

# -------------------------------------------------------
# OUTSTANDING ACTIONS
# -------------------------------------------------------

st.subheader("📋 Outstanding Actions")

st.dataframe(
    overdue_actions(actions),
    use_container_width=True
)

st.divider()

# -------------------------------------------------------
# DOWNLOAD
# -------------------------------------------------------

csv = display_kpis.to_csv(index=False)

st.download_button(
    label="📥 Download KPI Report",
    data=csv,
    file_name="Strategic_KPI_Report.csv",
    mime="text/csv"
)
