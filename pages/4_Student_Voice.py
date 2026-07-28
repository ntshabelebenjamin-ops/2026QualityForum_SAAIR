import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_student_voice

st.set_page_config(
    page_title="Student Voice",
    page_icon="🗣",
    layout="wide"
)

st.title("🗣 Student Voice Dashboard")

st.caption(
    "Student feedback, satisfaction, sentiment and experience"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

voice = load_student_voice()

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

programmes = ["All"] + sorted(
    voice["ProgrammeID"].dropna().unique().tolist()
)

selected_programme = st.sidebar.selectbox(
    "Programme",
    programmes
)

filtered = voice.copy()

if selected_programme != "All":
    filtered = filtered[
        filtered["ProgrammeID"] == selected_programme
    ]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

# Convert numeric columns safely
numeric_columns = [
    "OverallSatisfaction",
    "TeachingQuality",
    "AssessmentFeedback",
    "LearningResources",
    "StudentSupport",
    "DigitalLearning",
    "CampusFacilities"
]

for col in numeric_columns:
    if col in filtered.columns:
        filtered[col] = pd.to_numeric(
            filtered[col],
            errors="coerce"
        )

responses = len(filtered)

avg_satisfaction = round(
    filtered["OverallSatisfaction"].mean(skipna=True),
    2
)

# ---------------------------------------------------
# RECOMMENDATION SCORE
# ---------------------------------------------------

if "LikelihoodToRecommend" in filtered.columns:

    recommend_col = filtered["LikelihoodToRecommend"]

    # Try numeric first
    recommend_numeric = pd.to_numeric(
        recommend_col,
        errors="coerce"
    )

    if recommend_numeric.notna().sum() > 0:

        recommendation = round(
            recommend_numeric.mean(),
            2
        )

    else:

        # Handle Yes / No values
        yes_rate = (
            recommend_col
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("YES")
            .mean()
        )

        if pd.isna(yes_rate):

            recommendation = "N/A"

        else:

            recommendation = f"{yes_rate * 100:.1f}%"

else:

    recommendation = "N/A"

positive = (
    filtered["Sentiment"]
    .astype(str)
    .str.strip()
    .str.title()
    .eq("Positive")
    .sum()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Responses",
    responses
)

c2.metric(
    "Overall Satisfaction",
    avg_satisfaction
)

c3.metric(
    "Recommend SMU",
    recommendation
)

c4.metric(
    "Positive Comments",
    positive
)

st.divider()

# ---------------------------------------------------
# SATISFACTION SCORES
# ---------------------------------------------------

dimensions = [
    "TeachingQuality",
    "AssessmentFeedback",
    "LearningResources",
    "StudentSupport",
    "DigitalLearning",
    "CampusFacilities"
]

scores = []

for item in dimensions:
    scores.append(filtered[item].mean())

dimension_df = pd.DataFrame({
    "Dimension": dimensions,
    "Score": scores
})

fig = px.bar(
    dimension_df,
    x="Dimension",
    y="Score",
    title="Average Satisfaction Scores",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# SENTIMENT
# ---------------------------------------------------

sentiment = (
    filtered["Sentiment"]
    .value_counts()
    .reset_index()
)

sentiment.columns = [
    "Sentiment",
    "Count"
]

fig2 = px.pie(
    sentiment,
    values="Count",
    names="Sentiment",
    hole=0.55,
    title="Student Sentiment"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------------
# COMMENTS
# ---------------------------------------------------

st.subheader("Student Comments")

comments = filtered[
    [
        "ProgrammeID",
        "Comment",
        "Sentiment"
    ]
]

st.dataframe(
    comments,
    use_container_width=True
)

# ---------------------------------------------------
# AI INSIGHT
# ---------------------------------------------------

st.subheader("🤖 AI Student Voice Insight")

lowest_dimension = dimension_df.loc[
    dimension_df["Score"].idxmin()
]

highest_dimension = dimension_df.loc[
    dimension_df["Score"].idxmax()
]

st.info(f"""
Students rated **{highest_dimension['Dimension']}** highest
with an average score of **{highest_dimension['Score']:.2f}**.

The lowest rated area is **{lowest_dimension['Dimension']}**
with an average score of **{lowest_dimension['Score']:.2f}**.

Recommendation:

• Improve the lowest-performing service area.

• Review recurring student comments.

• Monitor satisfaction trends in future surveys.

• Link findings to programme review improvement plans.
""")

st.divider()

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Student Voice Report",
    csv,
    "Student_Voice_Report.csv",
    "text/csv"
)
