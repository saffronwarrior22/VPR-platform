import os
from typing import Optional, List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# Load variables from .env
load_dotenv()


class RangeRule(BaseModel):
    min: Optional[float] = Field(default=None)
    max: Optional[float] = Field(default=None)


class TrialCriteria(BaseModel):
    age: Optional[RangeRule] = None
    disease_duration_years: Optional[RangeRule] = None
    bmi: Optional[RangeRule] = None
    systolic_bp: Optional[RangeRule] = None
    diastolic_bp: Optional[RangeRule] = None
    hba1c: Optional[RangeRule] = None
    fasting_glucose: Optional[RangeRule] = None
    cholesterol: Optional[RangeRule] = None
    distance_from_trial_site_km: Optional[RangeRule] = None

    primary_disease: Optional[str] = None
    gender: Optional[List[str]] = None
    location: Optional[List[str]] = None
    disease_severity: Optional[List[str]] = None
    kidney_function: Optional[List[str]] = None
    liver_function: Optional[List[str]] = None
    availability: Optional[List[str]] = None
    consent_to_contact: Optional[List[str]] = None
    recent_surgery: Optional[List[str]] = None
    other_serious_condition: Optional[List[str]] = None
    pregnancy_status: Optional[List[str]] = None
    smoking_status: Optional[List[str]] = None
    alcohol_use: Optional[List[str]] = None

    exclude_comorbidities: Optional[List[str]] = None
    exclude_allergies: Optional[List[str]] = None
    exclude_previous_treatments: Optional[List[str]] = None


SYSTEM_PROMPT = """
You are a clinical-trial eligibility criteria extraction assistant.

Convert the trial eligibility text into structured criteria for the exact
patient schema supplied below.

Important:
- Extract only criteria explicitly stated or unambiguously implied.
- Do not invent medical thresholds.
- If a criterion is absent, return null for that field.
- Use the dataset's vocabulary where possible.
- This JSON will be consumed by a deterministic Python screening engine.
- Do NOT decide which patients are eligible.
- Do NOT provide medical advice.

Patient dataset fields:
age, gender, location, primary_disease, disease_duration_years,
disease_severity, comorbidities, previous_treatment, bmi, systolic_bp,
diastolic_bp, hba1c, fasting_glucose, kidney_function, liver_function,
cholesterol, smoking_status, alcohol_use, pregnancy_status, allergies,
recent_surgery, other_serious_condition, distance_from_trial_site_km,
availability, contact_preference, consent_to_contact, recruitment_status.

For exclusions:
- "no kidney disease" -> exclude_comorbidities
- "no penicillin allergy" -> exclude_allergies
- "must not have used insulin" -> exclude_previous_treatments

Return ONLY structured data matching the supplied schema.
"""


def parse_trial_criteria(trial_text: str) -> TrialCriteria:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    # Use GEMINI_MODEL from .env.
    # If it is not present, use the currently working model.
    model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    client = genai.Client(api_key=api_key)

    prompt = (
        SYSTEM_PROMPT
        + "\n\nTRIAL ELIGIBILITY TEXT:\n"
        + trial_text
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TrialCriteria,
            temperature=0,
        ),
    )

    return TrialCriteria.model_validate_json(response.text)