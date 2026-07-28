import streamlit as st
import pandas as pd

from utils.data_loader import (
    load_kpis,
    load_programme_reviews,
    load_student_success,
    load_student_voice,
    load_risks,
    load_improvement_plans
)

st.set_page_config(
    page_title="AI Decision Support",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 QAInsight AI Decision Support")

st.caption(
    "AI-powered institutional intelligence for evidence-based quality assurance and strategic decision-making."
)

# ==========================================================
# LOAD DATA
# ==========================================================

kpis = load_kpis()
reviews = load_programme_reviews()
students = load_student_success()
voice = load_student_voice()
risks = load_risks()
plans = load_improvement_plans()

# ==========================================================
# INSTITUTIONAL HEALTH SCORE
# ==========================================================

kpi_score = kpis["PerformancePercent"].mean()
review_score = reviews["OverallScore"].mean()
student_score = students["GraduationLikelihood"].mean()
voice_score = voice["OverallSatisfaction"].mean() * 20

high_risks = (risks["RiskLevel"] == "High").sum()

risk_score = max(0, 100 - (high_risks * 5))

health = round(
    (
        kpi_score * 0.30 +
        review_score * 0.25 +
        student_score * 0.20 +
        voice_score * 0.15 +
        risk_score * 0.10
    ),
    1
)

# ==========================================================
# STATUS
# ==========================================================

if health >= 90:
    status = "🟢 Excellent"

elif health >= 75:
    status = "🟡 Good"

elif health >= 60:
    status = "🟠 Needs Attention"

else:
    status = "🔴 Critical"

c1, c2 = st.columns(2)

c1.metric(
    "Institutional Health Score",
    f"{health}%"
)

c2.metric(
    "Overall Status",
    status
)

st.divider()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("Executive Summary")

st.markdown(f"""
### Institutional Performance Snapshot

- Institutional Health Score: **{health}%**
- Strategic KPI Performance: **{kpi_score:.1f}%**
- Programme Review Score: **{review_score:.1f}%**
- Graduate Success Indicator: **{student_score:.1f}%**
- Student Satisfaction Index: **{voice_score:.1f}%**
- High Institutional Risks: **{high_risks}**
""")

# ==========================================================
# PRIORITY RISKS
# ==========================================================

st.subheader("Highest Institutional Risks")

high = risks[
    risks["RiskLevel"] == "High"
]

if high.empty:

    st.success("No high institutional risks identified.")

else:

    st.dataframe(
        high,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# IMPROVEMENT PLANS
# ==========================================================

st.subheader("Improvement Plans")

outstanding = plans[
    plans["Status"] != "Completed"
]

st.dataframe(
    outstanding,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# AI RECOMMENDATIONS
# ==========================================================

st.subheader("🤖 AI Recommendations")

recommendations = []

if kpi_score < 80:
    recommendations.append(
        "Improve strategic KPI performance through targeted interventions."
    )

if review_score < 80:
    recommendations.append(
        "Prioritise programme reviews with low quality scores."
    )

if student_score < 80:
    recommendations.append(
        "Strengthen student success initiatives and academic support."
    )

if voice_score < 80:
    recommendations.append(
        "Improve the student experience by addressing satisfaction survey findings."
    )

if high_risks > 3:
    recommendations.append(
        "Escalate enterprise risks to Executive Management for mitigation."
    )

if len(recommendations) == 0:
    st.success(
        "Institutional performance is healthy. Continue monitoring key quality indicators and sustain current improvement initiatives."
    )

else:

    for i, item in enumerate(recommendations, 1):
        st.write(f"**{i}.** {item}")

# ==========================================================
# NEXT QUARTER PRIORITIES
# ==========================================================

st.subheader("Next Quarter Priorities")

priority_table = pd.DataFrame({

    "Priority":[
        "Strategic KPIs",
        "Programme Quality",
        "Student Success",
        "Institutional Risk",
        "Continuous Improvement"
    ],

    "Recommended Action":[
        "Monitor KPIs below target",
        "Implement review recommendations",
        "Support at-risk students",
        "Mitigate high enterprise risks",
        "Close overdue improvement plans"
    ]
})

st.dataframe(
    priority_table,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# ASK QAINSIGHT AI
# ==========================================================

st.subheader("Ask QAInsight AI")

question = st.text_input(
    "Ask an institutional quality question"
)

if question:

    q = question.lower()

    if "student" in q:

        st.info(
            f"The student success indicator is currently **{student_score:.1f}%**. Focus on students identified as high academic risk and monitor progression trends."
        )

    elif "programme" in q:

        st.info(
            f"The average programme review score is **{review_score:.1f}%**. Priority should be given to programmes with lower review scores and outstanding recommendations."
        )

    elif "risk" in q:

        st.info(
            f"There are currently **{high_risks}** high institutional risks recorded. These should be reviewed regularly with responsible offices."
        )

    elif "kpi" in q or "strategy" in q:

        st.info(
            f"The overall strategic KPI performance is **{kpi_score:.1f}%**. Focus on objectives that are below institutional targets."
        )

    else:

        st.info(
            "QAInsight AI analysed your question. Review the Executive Dashboard, Strategic KPIs, Programme Reviews and Student Success pages for supporting evidence before making institutional decisions."
        )
