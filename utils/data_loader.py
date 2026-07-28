import pandas as pd

# ==========================================================
# Generic CSV Loader
# ==========================================================

def _load_csv(path, numeric_cols=None, date_cols=None):
    """
    Generic loader with automatic data cleaning.
    """

    df = pd.read_csv(path)

    # Convert numeric columns
    if numeric_cols:
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert dates
    if date_cols:
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


# ==========================================================
# Executive Dashboard
# ==========================================================

def load_kpis():
    return _load_csv(
        "data/institutional/strategic_kpis.csv",
        numeric_cols=[
            "AnnualTarget",
            "CurrentPerformance",
            "PerformancePercent"
        ]
    )


def load_risks():
    return _load_csv(
        "data/institutional/institutional_risk_register.csv",
        numeric_cols=[
            "Likelihood",
            "Impact",
            "RiskScore"
        ]
    )


def load_actions():
    return _load_csv(
        "data/operations/action_tracker.csv",
        numeric_cols=[
            "ProgressPercent"
        ],
        date_cols=[
            "StartDate",
            "DueDate",
            "CompletionDate"
        ]
    )


# ==========================================================
# Teaching & Learning
# ==========================================================

def load_modules():
    return _load_csv(
        "data/academic/modules.csv",
        numeric_cols=[
            "Credits",
            "PassRate",
            "FailureRate",
            "AverageMark"
        ]
    )


def load_programme_reviews():
    return _load_csv(
        "data/academic/programme_reviews.csv",
        numeric_cols=[
            "OverallScore"
        ]
    )


def load_curriculum():
    return _load_csv(
        "data/academic/curriculum_mapping.csv"
    )


def load_ser():
    return _load_csv(
        "data/academic/self_evaluation_reports.csv"
    )


# ==========================================================
# Students
# ==========================================================

def load_students():
    return _load_csv(
        "data/students/students.csv",
        numeric_cols=[
            "AgeGroup",
            "GPA",
            "CreditsCompleted",
            "CreditsRegistered",
            "AttendanceRate"
        ]
    )


def load_student_success():
    return _load_csv(
        "data/students/student_success.csv",
        numeric_cols=[
            "ModulesPassed",
            "ModulesFailed",
            "CreditsEarned",
            "CreditsAttempted",
            "GraduationLikelihood"
        ]
    )


def load_graduate_readiness():
    return _load_csv(
        "data/students/graduate_readiness.csv",
        numeric_cols=[
            "CriticalThinking",
            "Communication",
            "Teamwork",
            "Leadership",
            "DigitalLiteracy",
            "AILiteracy",
            "ProblemSolving",
            "EthicalPractice",
            "Entrepreneurship",
            "OverallReadiness"
        ]
    )


def load_student_voice():
    return _load_csv(
        "data/students/student_voice.csv",
        numeric_cols=[
            "TeachingQuality",
            "AssessmentFeedback",
            "LearningResources",
            "StudentSupport",
            "DigitalLearning",
            "CampusFacilities",
            "OverallSatisfaction",
            "LikelihoodToRecommend"
        ]
    )


def load_graduate_destination():
    return _load_csv(
        "data/students/graduate_destination.csv",
        numeric_cols=[
            "MonthsToEmployment"
        ]
    )


# ==========================================================
# Institutional
# ==========================================================

def load_quality_standards():
    return _load_csv(
        "data/institutional/quality_standards.csv",
        numeric_cols=[
            "ComplianceScore"
        ]
    )


def load_app():
    return _load_csv(
        "data/institutional/annual_performance_plan.csv",
        numeric_cols=[
            "AnnualTarget",
            "QuarterTarget",
            "ActualPerformance",
            "Variance"
        ]
    )


# ==========================================================
# Operations
# ==========================================================

def load_complaints():
    return _load_csv(
        "data/operations/complaints.csv",
        numeric_cols=[
            "ResolutionDays"
        ],
        date_cols=[
            "ComplaintDate",
            "ResolutionDate"
        ]
    )


def load_improvement_plans():
    return _load_csv(
        "data/operations/improvement_plans.csv",
        numeric_cols=[
            "ProgressPercent"
        ],
        date_cols=[
            "StartDate",
            "DueDate"
        ]
    )


def load_evidence():
    return _load_csv(
        "data/operations/evidence_register.csv",
        date_cols=[
            "LastUpdated",
            "ExpiryDate"
        ]
    )


def load_audit_findings():
    return _load_csv(
        "data/operations/audit_findings.csv",
        date_cols=[
            "AuditDate",
            "TargetClosureDate"
        ]
    )

def load_improvement_plans():
    return _load_csv(
        "data/operations/quality_improvement_tracker.csv"
    )
