import pandas as pd


def load_kpis():

    return pd.read_csv(
        "data/institutional/strategic_kpis.csv"
    )


def load_students():

    return pd.read_csv(
        "data/students/students.csv"
    )


def load_voice():

    return pd.read_csv(
        "data/students/student_voice.csv"
    )


def load_success():

    return pd.read_csv(
        "data/students/student_success.csv"
    )


def load_SER():

    return pd.read_csv(
        "data/academic/self_evaluation_reports.csv"
    )


def load_reviews():

    return pd.read_csv(
        "data/academic/programme_reviews.csv"
    )


def load_actions():

    return pd.read_csv(
        "data/operations/action_tracker.csv"
    )

def load_modules():
    return pd.read_csv(
        "data/academic/modules.csv"
    )


def load_programme_reviews():
    return pd.read_csv(
        "data/academic/programme_reviews.csv"
    )


def load_curriculum():
    return pd.read_csv(
        "data/academic/curriculum_mapping.csv"
    )


def load_risks():

    return pd.read_csv(
        "data/institutional/institutional_risk_register.csv"
    )
