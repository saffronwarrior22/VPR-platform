# Virtual Patient Recruitment — Gemini + Rule Engine

Hackathon prototype for:
"An AI system that helps pharmaceutical companies find suitable patients for clinical trials."

## Architecture

Clinical-trial text
        ↓
Gemini LLM
        ↓
Structured eligibility criteria (JSON)
        ↓
Deterministic Python screening engine
        ↓
Candidate scoring + reasons
        ↓
Streamlit dashboard

Gemini is used to understand unstructured trial eligibility criteria.
The final patient screening decision is made by deterministic Python rules.

## Dataset

Put your uploaded file in this folder with the exact name:

`patients_5000_28.csv`

The expected columns are:

`patient_id, age, gender, location, primary_disease, disease_duration_years,
disease_severity, comorbidities, previous_treatment, bmi, systolic_bp,
diastolic_bp, hba1c, fasting_glucose, kidney_function, liver_function,
cholesterol, smoking_status, alcohol_use, pregnancy_status, allergies,
recent_surgery, other_serious_condition, distance_from_trial_site_km,
availability, contact_preference, consent_to_contact, recruitment_status`

## Setup

1. Install Python 3.10+.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` from `.env.example`.
5. Add your Gemini API key.
6. Copy `patients_5000_28.csv` into this project directory.
7. Run:

```bash
streamlit run app.py
```

## Demo trial criteria

Try:

Find adults aged 18-65 with Type 2 Diabetes, disease duration of at least
2 years, moderate or severe disease, BMI below 35, normal or mild kidney
function, normal or mild liver function, no recent surgery, no other serious
condition, within 50 km of the trial site, available for the trial, and
consented to contact.
