import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="QAInsight AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Header
# -----------------------------
st.title("🎓 QAInsight AI")

st.subheader(
    "AI-Powered Quality Assurance Decision Support System"
)

st.markdown("""
Supporting evidence-based decision-making through:

- 📊 Strategic Institutional Planning
- 🎓 Student Success Analytics
- 🗣 Student Voice
- 📚 Programme Reviews
- 📈 Strategic KPIs
- ⚠ Institutional Risk Management
- 🤖 AI Decision Support
- 📄 Executive Reporting
""")

st.divider()

# -----------------------------
# Quick Statistics
# -----------------------------
st.header("Institution Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Programmes", "10")

with col2:
    st.metric("Students", "2,500")

with col3:
    st.metric("Strategic KPIs", "40")

with col4:
    st.metric("Institutional Health", "91%")

st.divider()

# -----------------------------
# Feature Cards
# -----------------------------
st.header("Platform Modules")

c1, c2 = st.columns(2)

with c1:

    st.info("""
### 📊 Executive Dashboard

Monitor institutional performance,
KPIs,
risk,
continuous improvement,
and executive summaries.
""")

    st.info("""
### 🎓 Student Success

Analyse

- GPA
- Attendance
- Retention
- Progression
- Graduation likelihood
""")

    st.info("""
### 🗣 Student Voice

Analyse:

- Satisfaction
- Survey comments
- Sentiment
- Student experience
""")

with c2:

    st.info("""
### 📚 Programme Reviews

Monitor:

- SERs
- Accreditation
- Programme Reviews
- Curriculum Mapping
""")

    st.info("""
### ⚠ Continuous Improvement

Track:

- Complaints
- Audit Findings
- Improvement Plans
- Action Tracker
""")

    st.info("""
### 🤖 Ask QAInsight AI

Natural-language institutional analytics.

Example questions:

• Which KPIs are off track?

• Which programmes need attention?

• Summarise student satisfaction.

• Which actions are overdue?
""")

st.divider()

# -----------------------------
# Footer
# -----------------------------
st.success(
    "Welcome to QAInsight AI — a demonstration platform for AI-enabled Quality Assurance in Higher Education."
)
