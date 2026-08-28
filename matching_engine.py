import pandas as pd


NUMERIC_FIELDS = {
    "age": "age",
    "disease_duration_years": "disease_duration_years",
    "bmi": "bmi",
    "systolic_bp": "systolic_bp",
    "diastolic_bp": "diastolic_bp",
    "hba1c": "hba1c",
    "fasting_glucose": "fasting_glucose",
    "cholesterol": "cholesterol",
    "distance_from_trial_site_km": "distance_from_trial_site_km",
}

TEXT_FIELDS = {
    "gender": "gender",
    "location": "location",
    "primary_disease": "primary_disease",
    "disease_severity": "disease_severity",
    "kidney_function": "kidney_function",
    "liver_function": "liver_function",
    "availability": "availability",
    "consent_to_contact": "consent_to_contact",
    "recent_surgery": "recent_surgery",
    "other_serious_condition": "other_serious_condition",
    "pregnancy_status": "pregnancy_status",
    "smoking_status": "smoking_status",
    "alcohol_use": "alcohol_use",
}


def norm(value):
    """Normalize text for comparison."""
    if pd.isna(value):
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


def criteria_dict(criteria):
    """
    Convert Pydantic TrialCriteria or dictionary into dictionary.
    """
    if hasattr(criteria, "model_dump"):
        return criteria.model_dump(exclude_none=True)

    return criteria


def value_matches(value, allowed_values):
    """
    Flexible text matching.

    Example:
    'Type 2 Diabetes' matches 'type 2 diabetes'
    """
    value = norm(value)

    if not value:
        return False

    for item in allowed_values or []:
        item = norm(item)

        if value == item:
            return True

        if item in value or value in item:
            return True

    return False


def screen_patients(df, criteria):
    """
    Deterministic clinical-trial eligibility screening.

    Returns:
        eligible_df
        audit_df
    """

    criteria = criteria_dict(criteria)

    data = df.copy()

    eligible = pd.Series(True, index=data.index)

    # Store failure reasons for every patient.
    failure_reasons = {
        idx: []
        for idx in data.index
    }

    def apply_numeric(field, rule, label):
        nonlocal eligible

        if not rule:
            return

        col = NUMERIC_FIELDS.get(field)

        if not col or col not in data.columns:
            return

        values = pd.to_numeric(
            data[col],
            errors="coerce"
        )

        mask = pd.Series(True, index=data.index)

        if rule.get("min") is not None:
            mask &= values >= float(rule["min"])

        if rule.get("max") is not None:
            mask &= values <= float(rule["max"])

        failed = eligible & ~mask

        for idx in data.index[failed]:
            failure_reasons[idx].append(
                f"{label} does not meet the required range"
            )

        eligible &= mask

    def apply_text_list(field, values, label):
        nonlocal eligible

        if not values:
            return

        col = TEXT_FIELDS.get(field)

        if not col or col not in data.columns:
            return

        mask = data[col].map(
            lambda x: value_matches(x, values)
        )

        failed = eligible & ~mask

        for idx in data.index[failed]:
            failure_reasons[idx].append(
                f"{label} does not match the required value"
            )

        eligible &= mask

    # -----------------------------
    # Numeric criteria
    # -----------------------------

    apply_numeric(
        "age",
        criteria.get("age"),
        "Age"
    )

    apply_numeric(
        "disease_duration_years",
        criteria.get("disease_duration_years"),
        "Disease duration"
    )

    apply_numeric(
        "bmi",
        criteria.get("bmi"),
        "BMI"
    )

    apply_numeric(
        "systolic_bp",
        criteria.get("systolic_bp"),
        "Systolic BP"
    )

    apply_numeric(
        "diastolic_bp",
        criteria.get("diastolic_bp"),
        "Diastolic BP"
    )

    apply_numeric(
        "hba1c",
        criteria.get("hba1c"),
        "HbA1c"
    )

    apply_numeric(
        "fasting_glucose",
        criteria.get("fasting_glucose"),
        "Fasting glucose"
    )

    apply_numeric(
        "cholesterol",
        criteria.get("cholesterol"),
        "Cholesterol"
    )

    apply_numeric(
        "distance_from_trial_site_km",
        criteria.get("distance_from_trial_site_km"),
        "Distance"
    )

    # -----------------------------
    # Text criteria
    # -----------------------------

    apply_text_list(
        "gender",
        criteria.get("gender"),
        "Gender"
    )

    apply_text_list(
        "location",
        criteria.get("location"),
        "Location"
    )

    apply_text_list(
        "disease_severity",
        criteria.get("disease_severity"),
        "Disease severity"
    )

    apply_text_list(
        "kidney_function",
        criteria.get("kidney_function"),
        "Kidney function"
    )

    apply_text_list(
        "liver_function",
        criteria.get("liver_function"),
        "Liver function"
    )

    apply_text_list(
        "availability",
        criteria.get("availability"),
        "Availability"
    )

    apply_text_list(
        "consent_to_contact",
        criteria.get("consent_to_contact"),
        "Consent"
    )

    apply_text_list(
        "recent_surgery",
        criteria.get("recent_surgery"),
        "Recent surgery"
    )

    apply_text_list(
        "other_serious_condition",
        criteria.get("other_serious_condition"),
        "Serious condition"
    )

    apply_text_list(
        "pregnancy_status",
        criteria.get("pregnancy_status"),
        "Pregnancy status"
    )

    apply_text_list(
        "smoking_status",
        criteria.get("smoking_status"),
        "Smoking status"
    )

    apply_text_list(
        "alcohol_use",
        criteria.get("alcohol_use"),
        "Alcohol use"
    )

    # -----------------------------
    # Primary disease
    # -----------------------------

    disease = criteria.get("primary_disease")

    if disease and "primary_disease" in data.columns:

        mask = data["primary_disease"].map(
            lambda x: value_matches(x, [disease])
        )

        failed = eligible & ~mask

        for idx in data.index[failed]:
            failure_reasons[idx].append(
                "Primary disease does not match"
            )

        eligible &= mask

    # -----------------------------
    # Exclude comorbidities
    # -----------------------------

    if criteria.get("exclude_comorbidities"):

        terms = [
            norm(x)
            for x in criteria["exclude_comorbidities"]
        ]

        if "comorbidities" in data.columns:

            def has_excluded_comorbidity(value):
                text = norm(value)

                return any(
                    term in text
                    for term in terms
                )

            mask = ~data["comorbidities"].map(
                has_excluded_comorbidity
            )

            failed = eligible & ~mask

            for idx in data.index[failed]:
                failure_reasons[idx].append(
                    "Excluded comorbidity present"
                )

            eligible &= mask

    # -----------------------------
    # Exclude allergies
    # -----------------------------

    if criteria.get("exclude_allergies"):

        terms = [
            norm(x)
            for x in criteria["exclude_allergies"]
        ]

        if "allergies" in data.columns:

            def has_excluded_allergy(value):
                text = norm(value)

                return any(
                    term in text
                    for term in terms
                )

            mask = ~data["allergies"].map(
                has_excluded_allergy
            )

            failed = eligible & ~mask

            for idx in data.index[failed]:
                failure_reasons[idx].append(
                    "Excluded allergy present"
                )

            eligible &= mask

    # -----------------------------
    # Exclude previous treatments
    # -----------------------------

    if criteria.get("exclude_previous_treatments"):

        terms = [
            norm(x)
            for x in criteria["exclude_previous_treatments"]
        ]

        if "previous_treatment" in data.columns:

            def has_excluded_treatment(value):
                text = norm(value)

                return any(
                    term in text
                    for term in terms
                )

            mask = ~data["previous_treatment"].map(
                has_excluded_treatment
            )

            failed = eligible & ~mask

            for idx in data.index[failed]:
                failure_reasons[idx].append(
                    "Excluded previous treatment present"
                )

            eligible &= mask

    # -----------------------------
    # Audit dataframe
    # -----------------------------

    audit = data.copy()

    audit["eligible"] = eligible

    audit["screening_status"] = audit["eligible"].map(
        lambda x: "Eligible" if x else "Not Eligible"
    )

    audit["failure_reasons"] = [
        "; ".join(failure_reasons[idx])
        if failure_reasons[idx]
        else "All screening criteria satisfied"
        for idx in data.index
    ]

    # -----------------------------
    # Match score
    # -----------------------------

    audit["match_score"] = audit.apply(
        lambda row: calculate_score(
            row,
            criteria
        ),
        axis=1
    )

    audit["match_label"] = audit[
        "match_score"
    ].map(score_label)

    audit["explanation"] = audit.apply(
        lambda row: build_explanation(
            row,
            criteria
        ),
        axis=1
    )

    eligible_df = audit[
        audit["eligible"]
    ].sort_values(
        ["match_score", "distance_from_trial_site_km"],
        ascending=[False, True]
    )

    return eligible_df, audit


def calculate_score(row, criteria):

    score = 0

    # Consent
    if norm(row.get("consent_to_contact")) == "yes":
        score += 20

    # Availability
    availability = norm(
        row.get("availability")
    )

    if availability == "high":
        score += 15

    elif availability == "medium":
        score += 8

    # Distance
    distance = pd.to_numeric(
        row.get("distance_from_trial_site_km"),
        errors="coerce"
    )

    if pd.notna(distance):

        distance_rule = (
            criteria.get(
                "distance_from_trial_site_km"
            )
            or {}
        )

        max_distance = distance_rule.get("max")

        if max_distance is not None:

            ratio = max(
                0,
                1 - (
                    float(distance)
                    / float(max_distance)
                )
            )

            score += round(
                20 * ratio
            )

        elif distance <= 25:
            score += 20

        elif distance <= 50:
            score += 12

        elif distance <= 100:
            score += 5

    # Kidney function
    kidney = norm(
        row.get("kidney_function")
    )

    if kidney == "normal":
        score += 10

    elif kidney == "mild":
        score += 6

    # Liver function
    liver = norm(
        row.get("liver_function")
    )

    if liver == "normal":
        score += 10

    elif liver == "mild":
        score += 6

    # Serious condition
    if norm(
        row.get("other_serious_condition")
    ) == "no":

        score += 10

    # Recent surgery
    if norm(
        row.get("recent_surgery")
    ) == "no":

        score += 5

    return min(score, 100)


def score_label(score):

    if score >= 85:
        return "Excellent Match"

    if score >= 70:
        return "Strong Match"

    if score >= 55:
        return "Potential Match"

    return "Lower Priority"


def build_explanation(row, criteria):

    positives = []

    if criteria.get("primary_disease"):

        if value_matches(
            row.get("primary_disease"),
            [criteria["primary_disease"]]
        ):

            positives.append(
                f"has {row['primary_disease']}"
            )

    if criteria.get("age"):

        positives.append(
            f"age {row['age']} is within the requested range"
        )

    if criteria.get("disease_duration_years"):

        positives.append(
            f"disease duration is "
            f"{row['disease_duration_years']} years"
        )

    if criteria.get("bmi"):

        positives.append(
            f"BMI is {row['bmi']}"
        )

    if criteria.get("hba1c"):

        positives.append(
            f"HbA1c is {row['hba1c']}"
        )

    if criteria.get("kidney_function"):

        positives.append(
            f"kidney function: "
            f"{row['kidney_function']}"
        )

    if criteria.get("liver_function"):

        positives.append(
            f"liver function: "
            f"{row['liver_function']}"
        )

    if norm(
        row.get("consent_to_contact")
    ) == "yes":

        positives.append(
            "consented to contact"
        )

    if norm(
        row.get("availability")
    ) in {"high", "medium"}:

        positives.append(
            f"availability: "
            f"{row['availability']}"
        )

    distance = row.get(
        "distance_from_trial_site_km"
    )

    if pd.notna(distance):

        positives.append(
            f"{distance} km from trial site"
        )

    if not positives:
        return (
            "Candidate meets the deterministic "
            "screening rules."
        )

    return (
        "Candidate meets the deterministic "
        "screening rules: "
        + "; ".join(positives)
        + "."
    )