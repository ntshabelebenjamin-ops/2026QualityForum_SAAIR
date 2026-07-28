import streamlit as st
import pandas as pd

from utils.data_loader import (
    load_kpis,
    load_programme_reviews,
    load_student_success,
    load_student_voice,
    load_risks,
    load_actions,
    load_improvement_plans
)

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Executive Reports")

st.caption(
    "Generate executive summaries and download institutional reports."
)

# =====================================================
# LOAD DATA
# =====================================================

kpis = load_kpis()
reviews = load_programme_reviews()
students = load_student_success()
voice = load_student_voice()
risks = load_risks()
actions = load_actions()
plans = load_improvement_plans()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

overall_kpi = round(kpis["PerformancePercent"].mean(), 1)
review_score = round(reviews["OverallScore"].mean(), 1)
student_success = round(students["GraduationLikelihood"].mean(), 1)
student_satisfaction = round(
    voice["OverallSatisfaction"].mean() * 20,
    1
)

high_risks = (risks["RiskLevel"] == "High").sum()

st.subheader("Executive Summary")

summary = pd.DataFrame({

    "Indicator":[
        "Strategic KPI Performance",
        "Programme Review Score",
        "Graduate Success",
        "Student Satisfaction",
        "High Institutional Risks"
    ],

    "Value":[
        f"{overall_kpi}%",
        f"{review_score}%",
        f"{student_success}%",
        f"{student_satisfaction}%",
        high_risks
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# REPORT DOWNLOADS
# =====================================================

st.subheader("Available Reports")

reports = {

    "Strategic KPIs": kpis,

    "Programme Reviews": reviews,

    "Student Success": students,

    "Student Voice": voice,

    "Institutional Risks": risks,

    "Action Tracker": actions,

    "Improvement Plans": plans

}

for name, df in reports.items():

    st.markdown(f"### {name}")

    st.write(f"Records: **{len(df)}**")

    csv = df.to_csv(index=False)

    st.download_button(
        label=f"📥 Download {name}",
        data=csv,
        file_name=f"{name.replace(' ','_')}.csv",
        mime="text/csv",
        key=name
    )

    st.divider()

# =====================================================
# EXECUTIVE NARRATIVE
# =====================================================

st.subheader("🤖 Executive Narrative")

st.markdown(f"""

### Institutional Performance Overview

The institution achieved an average Strategic KPI performance of **{overall_kpi}%**.

Programme quality reviews recorded an average score of **{review_score}%**, indicating the overall quality status across reviewed programmes.

Student success indicators currently average **{student_success}%**, while overall student satisfaction stands at **{student_satisfaction}%**.

The institutional risk register currently records **{high_risks}** high-risk items requiring ongoing monitoring and mitigation.

### Recommended Executive Priorities

1. Improve underperforming Strategic KPIs.

2. Complete outstanding programme review recommendations.

3. Reduce institutional risk exposure.

4. Strengthen student success initiatives.

5. Monitor implementation of improvement plans.

""")

# =====================================================
# MANAGEMENT DASHBOARD SNAPSHOT
# =====================================================

st.subheader("Management Dashboard Snapshot")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Strategic KPIs",
    f"{overall_kpi}%"
)

c2.metric(
    "Programme Reviews",
    f"{review_score}%"
)

c3.metric(
    "Student Success",
    f"{student_success}%"
)

c4.metric(
    "High Risks",
    high_risks
)

st.success(
    "Executive reports are ready for download and can support Council, Senate, Executive Management and Quality Committee reporting."
)
