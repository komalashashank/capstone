import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_FILE = BASE_DIR / "data" / "raw" / "student_data.csv"
PROCESSED_FILE = BASE_DIR / "data" / "processed" / "processed data.csv"

df = pd.read_csv(RAW_FILE)

print("Original shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

df["gender"] = df["gender"].fillna("Unknown")
df["major"] = df["major"].fillna("Unknown")
df["enrollment_status"] = df["enrollment_status"].fillna("Unknown")

numeric_cols = [
    "age",
    "GPA",
    "course_load",
    "avg_course_grade",
    "attendance_rate",
    "lms_logins_past_month",
    "avg_session_duration_minutes",
    "assignment_submission_rate",
    "forum_participation_count",
    "video_completion_rate"
]

# Convert invalid GPA values to missing
df.loc[(df["GPA"] < 0) | (df["GPA"] > 4), "GPA"] = np.nan

# Convert invalid attendance values to missing
df.loc[
    (df["attendance_rate"] < 0) |
    (df["attendance_rate"] > 1),
    "attendance_rate"
] = np.nan

# Fill missing numeric values using median
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Standardize risk-level labels
df["risk_level"] = df["risk_level"].str.strip().str.title()
df = df.dropna(subset=["student_id", "risk_level"])

df = df.drop_duplicates()

df = df.dropna(subset=["student_id", "risk_level"])

PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(PROCESSED_FILE, index=False)

print("\nProcessed shape:", df.shape)

print("\nRisk level counts:")
print(df["risk_level"].value_counts())

print("\nProcessing completed.")