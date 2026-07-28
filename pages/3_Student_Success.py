import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_students,
    load_student_success,
    load_graduate_readiness
)

st.set_page_config(
    page_title="Student Success",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Success Dashboard")

st.caption(
    "Student progression, retention, academic risk and graduate readiness"
)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

students = load_students()
success = load_student_success()
readiness = load_graduate_readiness()

# ----------------------------------------------------
# MERGE DATA
# ----------------------------------------------------

df = students.merge(
    success,
    on="StudentID",
    how="left"
)

df = df.merge(
    readiness,
    on="StudentID",
    how="left"
)

# ----------------------------------------------------
# FILTERS
# ----------------------------------------------------

schools = ["All"] + sorted(df["School"].dropna().unique())

selected_school = st.sidebar.selectbox(
    "School",
    schools
)

if selected_school != "All":
    df = df[df["School"] == selected_school]

# ----------------------------------------------------
# KPIs
# ----------------------------------------------------

total_students = len(df)

avg_gpa = round(df["GPA"].mean(),2)

retained = (
    df["RetentionStatus"] == "Retained"
).sum()

retention_rate = round(
    retained / total_students * 100,
    1
) if total_students else 0

high_risk = (
    df["AcademicRisk"] == "High"
).sum()

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Students",
    total_students
)

c2.metric(
    "Average GPA",
    avg_gpa
)

c3.metric(
    "Retention",
    f"{retention_rate}%"
)

c4.metric(
    "High Risk",
    high_risk
)

st.divider()

# ----------------------------------------------------
# GPA Distribution
# ----------------------------------------------------

fig = px.histogram(
    df,
    x="GPA",
    nbins=10,
    title="GPA Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Academic Risk
# ----------------------------------------------------

risk = (
    df["AcademicRisk"]
    .value_counts()
    .reset_index()
)

risk.columns = [
    "Risk",
    "Students"
]

fig2 = px.pie(
    risk,
    values="Students",
    names="Risk",
    hole=.5,
    title="Academic Risk Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------------------------------------------------
# Graduate Readiness
# ----------------------------------------------------

st.subheader("Graduate Readiness")

skills = [
    "CriticalThinking",
    "Communication",
    "Leadership",
    "DigitalLiteracy",
    "AILiteracy",
    "ProblemSolving"
]

skill_scores = []

for skill in skills:

    skill_scores.append(
        readiness[skill].mean()
    )

skills_df = pd.DataFrame({
    "Skill":skills,
    "Average":skill_scores
})

fig3 = px.bar(
    skills_df,
    x="Skill",
    y="Average",
    title="Graduate Readiness Skills"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ----------------------------------------------------
# High Risk Students
# ----------------------------------------------------

st.subheader("Students Requiring Intervention")

st.dataframe(
    df[
        df["AcademicRisk"]=="High"
    ],
    use_container_width=True
)

# ----------------------------------------------------
# AI Insight
# ----------------------------------------------------

st.subheader("🤖 AI Student Success Insight")

if high_risk == 0:

    st.success("""
No students are currently classified as
high academic risk.

Continue monitoring progression and
graduate readiness.
""")

else:

    st.warning(f"""
There are **{high_risk} students**
classified as high academic risk.

Recommended interventions include:

• Academic advising

• Tutoring support

• Attendance monitoring

• Student counselling

• Early warning notifications
""")

st.divider()

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Student Success Report",
    csv,
    "Student_Success_Report.csv",
    "text/csv"
)
