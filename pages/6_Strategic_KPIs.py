# ==========================================================
# CREATE KPI STATUS FROM PERFORMANCE
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

# Always derive status from PerformancePercent
kpis["Status"] = kpis["PerformancePercent"].apply(classify_status)

# ==========================================================
# KPI SUMMARY
# ==========================================================

overall = round(kpis["PerformancePercent"].mean(), 1)
total_kpis = len(kpis)

achieved = (kpis["Status"] == "Achieved").sum()
on_track = (kpis["Status"] == "On Track").sum()
at_risk = (kpis["Status"] == "At Risk").sum()

# Calculate overdue actions
if "DueDate" in actions.columns:

    actions["DueDate"] = pd.to_datetime(
        actions["DueDate"],
        errors="coerce"
    )

    overdue = (
        (actions["DueDate"] < pd.Timestamp.today()) &
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

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Overall Performance", f"{overall}%")
c2.metric("Total KPIs", total_kpis)
c3.metric("Achieved", achieved)
c4.metric("On Track", on_track)
c5.metric("At Risk", at_risk)

st.metric("Overdue Actions", overdue)

st.divider()
