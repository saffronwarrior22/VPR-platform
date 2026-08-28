import pandas as pd

from gemini_parser import parse_trial_criteria
from matching_engine import screen_patients


# Load patient dataset
df = pd.read_csv("patients_5000_28.csv")

print("\n===================================")
print("PATIENT DATASET")
print("===================================")

print("Total patients:", len(df))
print("Columns:", len(df.columns))


# Trial eligibility text
trial_text = """
Adults aged 18 to 65 years with Type 2 Diabetes.
BMI must be between 18 and 35.
HbA1c must be between 7 and 10.
Patients must have moderate disease severity.
Patients must not have kidney disease.
Patients must not have a penicillin allergy.
Patients must not have used insulin previously.
"""


# Step 1: Gemini extraction
print("\n===================================")
print("STEP 1: GEMINI CRITERIA EXTRACTION")
print("===================================")

criteria = parse_trial_criteria(trial_text)

print(
    criteria.model_dump_json(indent=2)
)


# Step 2: Deterministic screening
print("\n===================================")
print("STEP 2: PATIENT SCREENING")
print("===================================")

eligible, audit = screen_patients(
    df,
    criteria
)


# Results
print("\n===================================")
print("RESULTS")
print("===================================")

print(
    "Total patients:",
    len(df)
)

print(
    "Eligible patients:",
    len(eligible)
)

print(
    "Not eligible:",
    len(audit) - len(eligible)
)


# Top candidates
print("\n===================================")
print("TOP 10 CANDIDATES")
print("===================================")

columns = [
    "patient_id",
    "age",
    "gender",
    "primary_disease",
    "bmi",
    "hba1c",
    "match_score",
    "match_label",
    "explanation",
]

available_columns = [
    col for col in columns
    if col in eligible.columns
]

print(
    eligible[
        available_columns
    ].head(10).to_string(index=False)
)


# Save results
eligible.to_csv(
    "eligible_patients.csv",
    index=False
)

audit.to_csv(
    "screening_audit.csv",
    index=False
)

print("\n===================================")
print("FILES CREATED")
print("===================================")

print("eligible_patients.csv")
print("screening_audit.csv")

