import pandas as pd


def executive_summary(kpi_df):
    """
    Executive Summary from Strategic KPIs
    """

    total = len(kpi_df)

    exceeded = len(
        kpi_df[kpi_df["Status"] == "Exceeded Target"]
    )

    on_track = len(
        kpi_df[kpi_df["Status"] == "On Track"]
    )

    below = len(
        kpi_df[kpi_df["Status"] == "Below Target"]
    )

    off_track = len(
        kpi_df[kpi_df["Status"] == "Off Track"]
    )

    summary = f"""
## Executive Summary

Total KPIs monitored: **{total}**

✅ Exceeded Target: **{exceeded}**

🟢 On Track: **{on_track}**

🟡 Below Target: **{below}**

🔴 Off Track: **{off_track}**

Priority attention should be given to KPIs that are below target or off track.
"""

    return summary


def high_risk_items(df):

    return df[df["RiskLevel"] == "High"]


def overdue_actions(df):

    return df[df["Status"] == "Open"]


def improvement_progress(df):

    return round(
        df["ProgressPercent"].mean(),
        1
    )
