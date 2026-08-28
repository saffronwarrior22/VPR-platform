from gemini_parser import parse_trial_criteria

trial_text = """
Adults aged 18 to 65 years with Type 2 Diabetes.
BMI must be between 18 and 35.
HbA1c must be between 7 and 10.
Patients must have moderate disease severity.
Patients must not have kidney disease.
Patients must not have a penicillin allergy.
Patients must not have used insulin previously.
"""

criteria = parse_trial_criteria(trial_text)

print("\n===== EXTRACTED TRIAL CRITERIA =====\n")
print(criteria.model_dump_json(indent=2))