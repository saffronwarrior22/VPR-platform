import streamlit as st
import pandas as pd

from database import (
    initialize_database,
    import_csv_if_empty,
    load_patients,
    add_patient,
    patient_count,
)

from matching_engine import screen_patients


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Virtual Patient Recruitment AI",
    page_icon="🧬",
    layout="wide",
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()

import_csv_if_empty(
    "patients_5000_28.csv"
)


# ============================================================
# LOAD PATIENTS
# ============================================================

patients = load_patients()


# ============================================================
# HEADER
# ============================================================

st.title("🧬 Virtual Patient Recruitment AI")

st.caption(
    "Select clinical trial eligibility criteria and find matching patients."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ System Status")

    st.success("Patient Database Connected")

    st.success("Matching Engine Ready")

    st.metric(
        "Live Patients",
        patient_count()
    )

    st.divider()

    st.markdown(
        """
        ### How it works

        **1.** Select trial criteria.

        **2.** System creates structured rules.

        **3.** Python screens all patients.

        **4.** Matching patients are ranked.

        **5.** View patient details and results.
        """
    )


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "🔬 Trial Matching",
        "➕ Add Patient",
        "👥 Patient Database",
    ]
)


# ============================================================
# TRIAL MATCHING
# ============================================================

if page == "🔬 Trial Matching":

    st.header("🔬 Create Clinical Trial Criteria")

    st.write(
        "Select the requirements for your clinical trial."
    )

    # ========================================================
    # BASIC CRITERIA
    # ========================================================

    st.subheader("👤 Patient Demographics")

    col1, col2 = st.columns(2)

    with col1:

        age_enabled = st.checkbox(
            "Specify Age Range",
            value=True
        )

        if age_enabled:

            age_min, age_max = st.slider(
                "Age Range",
                min_value=0,
                max_value=100,
                value=(18, 65)
            )

        else:

            age_min = None
            age_max = None


    with col2:

        gender_enabled = st.checkbox(
            "Specify Gender"
        )

        if gender_enabled:

            gender = st.multiselect(
                "Allowed Gender",
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            )

        else:

            gender = None


    # ========================================================
    # DISEASE
    # ========================================================

    st.subheader("🧬 Disease Requirements")

    col1, col2, col3 = st.columns(3)

    with col1:

        disease_enabled = st.checkbox(
            "Specify Primary Disease",
            value=True
        )

        if disease_enabled:

            primary_disease = st.selectbox(
                "Primary Disease",
                [
                    "Type 2 Diabetes",
                    "Type 1 Diabetes",
                    "Hypertension",
                    "Heart Disease",
                    "Chronic Kidney Disease",
                    "Asthma",
                    "COPD",
                    "Cancer",
                    "Obesity",
                    "Other"
                ]
            )

        else:

            primary_disease = None


    with col2:

        severity_enabled = st.checkbox(
            "Specify Disease Severity"
        )

        if severity_enabled:

            disease_severity = st.multiselect(
                "Disease Severity",
                [
                    "Mild",
                    "Moderate",
                    "Severe"
                ]
            )

        else:

            disease_severity = None


    with col3:

        duration_enabled = st.checkbox(
            "Specify Disease Duration"
        )

        if duration_enabled:

            duration_min, duration_max = st.slider(
                "Disease Duration (Years)",
                min_value=0,
                max_value=50,
                value=(0, 20)
            )

        else:

            duration_min = None
            duration_max = None


    # ========================================================
    # CLINICAL MEASUREMENTS
    # ========================================================

    st.subheader("🩺 Clinical Measurements")

    col1, col2 = st.columns(2)

    with col1:

        bmi_enabled = st.checkbox(
            "Specify BMI Range",
            value=True
        )

        if bmi_enabled:

            bmi_min, bmi_max = st.slider(
                "BMI",
                min_value=10.0,
                max_value=60.0,
                value=(18.0, 35.0),
                step=0.5
            )

        else:

            bmi_min = None
            bmi_max = None


        hba1c_enabled = st.checkbox(
            "Specify HbA1c Range",
            value=True
        )

        if hba1c_enabled:

            hba1c_min, hba1c_max = st.slider(
                "HbA1c (%)",
                min_value=3.0,
                max_value=20.0,
                value=(7.0, 10.0),
                step=0.1
            )

        else:

            hba1c_min = None
            hba1c_max = None


        glucose_enabled = st.checkbox(
            "Specify Fasting Glucose"
        )

        if glucose_enabled:

            glucose_min, glucose_max = st.slider(
                "Fasting Glucose",
                min_value=40.0,
                max_value=500.0,
                value=(70.0, 150.0),
                step=1.0
            )

        else:

            glucose_min = None
            glucose_max = None


    with col2:

        systolic_enabled = st.checkbox(
            "Specify Systolic BP"
        )

        if systolic_enabled:

            systolic_min, systolic_max = st.slider(
                "Systolic BP",
                min_value=60,
                max_value=250,
                value=(90, 140)
            )

        else:

            systolic_min = None
            systolic_max = None


        diastolic_enabled = st.checkbox(
            "Specify Diastolic BP"
        )

        if diastolic_enabled:

            diastolic_min, diastolic_max = st.slider(
                "Diastolic BP",
                min_value=30,
                max_value=150,
                value=(60, 90)
            )

        else:

            diastolic_min = None
            diastolic_max = None


        cholesterol_enabled = st.checkbox(
            "Specify Cholesterol"
        )

        if cholesterol_enabled:

            cholesterol_min, cholesterol_max = st.slider(
                "Cholesterol",
                min_value=50,
                max_value=500,
                value=(100, 250)
            )

        else:

            cholesterol_min = None
            cholesterol_max = None


    # ========================================================
    # ORGAN FUNCTION
    # ========================================================

    st.subheader("🧪 Organ Function")

    col1, col2 = st.columns(2)

    with col1:

        kidney_enabled = st.checkbox(
            "Specify Kidney Function"
        )

        if kidney_enabled:

            kidney_function = st.multiselect(
                "Allowed Kidney Function",
                [
                    "Normal",
                    "Mild",
                    "Moderate",
                    "Severe"
                ]
            )

        else:

            kidney_function = None


    with col2:

        liver_enabled = st.checkbox(
            "Specify Liver Function"
        )

        if liver_enabled:

            liver_function = st.multiselect(
                "Allowed Liver Function",
                [
                    "Normal",
                    "Mild",
                    "Moderate",
                    "Severe"
                ]
            )

        else:

            liver_function = None


    # ========================================================
    # SAFETY / EXCLUSION CRITERIA
    # ========================================================

    st.subheader("🚫 Exclusion Criteria")

    col1, col2, col3 = st.columns(3)

    with col1:

        kidney_exclusion = st.checkbox(
            "Exclude Kidney Disease"
        )

        allergy_exclusion = st.checkbox(
            "Exclude Penicillin Allergy"
        )


    with col2:

        insulin_exclusion = st.checkbox(
            "Exclude Previous Insulin Treatment"
        )

        surgery_exclusion = st.checkbox(
            "Exclude Recent Surgery"
        )


    with col3:

        serious_condition_exclusion = st.checkbox(
            "Exclude Serious Conditions"
        )

        pregnancy_exclusion = st.checkbox(
            "Exclude Pregnancy"
        )


    # ========================================================
    # RECRUITMENT REQUIREMENTS
    # ========================================================

    st.subheader("📞 Recruitment Requirements")

    col1, col2, col3 = st.columns(3)

    with col1:

        consent_required = st.checkbox(
            "Require Contact Consent"
        )

    with col2:

        availability_required = st.checkbox(
            "Require Availability"
        )

    with col3:

        distance_enabled = st.checkbox(
            "Maximum Distance"
        )

        if distance_enabled:

            max_distance = st.number_input(
                "Maximum Distance (km)",
                min_value=1.0,
                max_value=1000.0,
                value=50.0
            )

        else:

            max_distance = None


    # ========================================================
    # SUMMARY
    # ========================================================

    st.divider()

    st.subheader("📋 Selected Trial Criteria")

    summary = []

    if age_enabled:

        summary.append(
            f"Age: {age_min}–{age_max}"
        )

    if gender_enabled and gender:

        summary.append(
            f"Gender: {', '.join(gender)}"
        )

    if disease_enabled:

        summary.append(
            f"Disease: {primary_disease}"
        )

    if severity_enabled and disease_severity:

        summary.append(
            f"Severity: {', '.join(disease_severity)}"
        )

    if duration_enabled:

        summary.append(
            f"Disease duration: {duration_min}–{duration_max} years"
        )

    if bmi_enabled:

        summary.append(
            f"BMI: {bmi_min}–{bmi_max}"
        )

    if hba1c_enabled:

        summary.append(
            f"HbA1c: {hba1c_min}–{hba1c_max}%"
        )

    if glucose_enabled:

        summary.append(
            f"Fasting glucose: {glucose_min}–{glucose_max}"
        )

    if systolic_enabled:

        summary.append(
            f"Systolic BP: {systolic_min}–{systolic_max}"
        )

    if diastolic_enabled:

        summary.append(
            f"Diastolic BP: {diastolic_min}–{diastolic_max}"
        )

    if cholesterol_enabled:

        summary.append(
            f"Cholesterol: {cholesterol_min}–{cholesterol_max}"
        )

    if kidney_enabled and kidney_function:

        summary.append(
            f"Kidney function: {', '.join(kidney_function)}"
        )

    if liver_enabled and liver_function:

        summary.append(
            f"Liver function: {', '.join(liver_function)}"
        )

    if kidney_exclusion:

        summary.append(
            "Exclude kidney disease"
        )

    if allergy_exclusion:

        summary.append(
            "Exclude penicillin allergy"
        )

    if insulin_exclusion:

        summary.append(
            "Exclude previous insulin treatment"
        )

    if surgery_exclusion:

        summary.append(
            "Exclude recent surgery"
        )

    if serious_condition_exclusion:

        summary.append(
            "Exclude serious conditions"
        )

    if pregnancy_exclusion:

        summary.append(
            "Exclude pregnancy"
        )

    if consent_required:

        summary.append(
            "Contact consent required"
        )

    if availability_required:

        summary.append(
            "Availability required"
        )

    if distance_enabled:

        summary.append(
            f"Maximum distance: {max_distance} km"
        )


    if summary:

        for item in summary:

            st.write(
                f"✓ {item}"
            )

    else:

        st.info(
            "No criteria selected."
        )


    # ========================================================
    # BUILD CRITERIA
    # ========================================================

    criteria = {

        "age": (
            {
                "min": age_min,
                "max": age_max
            }
            if age_enabled
            else None
        ),

        "gender": (
            gender
            if gender_enabled and gender
            else None
        ),

        "primary_disease": (
            primary_disease
            if disease_enabled
            else None
        ),

        "disease_severity": (
            disease_severity
            if severity_enabled and disease_severity
            else None
        ),

        "disease_duration_years": (
            {
                "min": duration_min,
                "max": duration_max
            }
            if duration_enabled
            else None
        ),

        "bmi": (
            {
                "min": bmi_min,
                "max": bmi_max
            }
            if bmi_enabled
            else None
        ),

        "hba1c": (
            {
                "min": hba1c_min,
                "max": hba1c_max
            }
            if hba1c_enabled
            else None
        ),

        "fasting_glucose": (
            {
                "min": glucose_min,
                "max": glucose_max
            }
            if glucose_enabled
            else None
        ),

        "systolic_bp": (
            {
                "min": systolic_min,
                "max": systolic_max
            }
            if systolic_enabled
            else None
        ),

        "diastolic_bp": (
            {
                "min": diastolic_min,
                "max": diastolic_max
            }
            if diastolic_enabled
            else None
        ),

        "cholesterol": (
            {
                "min": cholesterol_min,
                "max": cholesterol_max
            }
            if cholesterol_enabled
            else None
        ),

        "kidney_function": (
            kidney_function
            if kidney_enabled and kidney_function
            else None
        ),

        "liver_function": (
            liver_function
            if liver_enabled and liver_function
            else None
        ),

        "exclude_comorbidities": (
            ["kidney disease"]
            if kidney_exclusion
            else None
        ),

        "exclude_allergies": (
            ["penicillin"]
            if allergy_exclusion
            else None
        ),

        "exclude_previous_treatments": (
            ["insulin"]
            if insulin_exclusion
            else None
        ),

        "recent_surgery": (
            ["No"]
            if surgery_exclusion
            else None
        ),

        "other_serious_condition": (
            ["No"]
            if serious_condition_exclusion
            else None
        ),

        "pregnancy_status": (
            ["Not Pregnant"]
            if pregnancy_exclusion
            else None
        ),

        "consent_to_contact": (
            ["Yes"]
            if consent_required
            else None
        ),

        "availability": (
            ["High", "Medium"]
            if availability_required
            else None
        ),

        "distance_from_trial_site_km": (
            {
                "min": 0,
                "max": max_distance
            }
            if distance_enabled
            else None
        ),
    }


    # Remove None values

    criteria = {
        key: value
        for key, value in criteria.items()
        if value is not None
    }


    # ========================================================
    # MATCH BUTTON
    # ========================================================

    st.divider()

    if st.button(
        "🔍 Find Matching Patients",
        type="primary",
        use_container_width=True
    ):

        if not criteria:

            st.warning(
                "Please select at least one trial criterion."
            )

            st.stop()


        with st.spinner(
            f"Screening {len(patients):,} patients..."
        ):

            try:

                eligible, audit = screen_patients(
                    patients,
                    criteria
                )

            except Exception as e:

                st.error(
                    f"Screening failed: {e}"
                )

                st.stop()


        # ====================================================
        # RESULTS
        # ====================================================

        st.header("📊 Recruitment Results")

        total = len(audit)

        eligible_count = len(eligible)

        not_eligible = (
            total - eligible_count
        )

        match_rate = (
            eligible_count / total * 100
            if total
            else 0
        )


        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Patients",
            f"{total:,}"
        )

        c2.metric(
            "Eligible",
            f"{eligible_count:,}"
        )

        c3.metric(
            "Not Eligible",
            f"{not_eligible:,}"
        )

        c4.metric(
            "Match Rate",
            f"{match_rate:.1f}%"
        )


        # ====================================================
        # RESULTS TABLE
        # ====================================================

        st.subheader(
            "🏆 Top Matching Patients"
        )

        if eligible.empty:

            st.warning(
                "No patients match the selected criteria."
            )

        else:

            display_columns = [
                "patient_id",
                "age",
                "gender",
                "primary_disease",
                "bmi",
                "hba1c",
                "match_score",
                "match_label",
                "distance_from_trial_site_km",
            ]

            display_columns = [
                col
                for col in display_columns
                if col in eligible.columns
            ]

            st.dataframe(
                eligible[
                    display_columns
                ].head(50),
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # PATIENT DETAILS
            # =================================================

            st.subheader(
                "👤 Patient Details"
            )

            selected_id = st.selectbox(
                "Select a patient",
                eligible[
                    "patient_id"
                ].astype(str).tolist()
            )


            selected = eligible[
                eligible[
                    "patient_id"
                ].astype(str)
                == selected_id
            ].iloc[0]


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"### Patient {selected_id}"
                )

                patient_details = selected[
                    [
                        col
                        for col in patients.columns
                        if col in selected.index
                    ]
                ]

                st.dataframe(
                    patient_details.to_frame(
                        "Value"
                    ),
                    use_container_width=True
                )


            with col2:

                st.write(
                    "### 🎯 Match Assessment"
                )

                st.metric(
                    "Match Score",
                    f"{selected['match_score']}/100"
                )

                st.success(
                    selected["match_label"]
                )

                st.info(
                    selected["explanation"]
                )


            # =================================================
            # DOWNLOAD
            # =================================================

            csv = eligible.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Eligible Patients",
                csv,
                "eligible_patients.csv",
                "text/csv",
                use_container_width=True
            )


# ============================================================
# ADD PATIENT
# ============================================================

elif page == "➕ Add Patient":

    st.header("➕ Add New Patient")

    st.info(
        "New patients are stored in the live patient database "
        "and will be included in future trial screening."
    )


    with st.form("patient_form"):

        col1, col2, col3 = st.columns(3)

        with col1:

            patient_id = st.text_input(
                "Patient ID"
            )

            age = st.number_input(
                "Age",
                0,
                120,
                40
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            )

        with col2:

            location = st.text_input(
                "Location",
                "Aurangabad"
            )

            disease = st.text_input(
                "Primary Disease",
                "Type 2 Diabetes"
            )

            duration = st.number_input(
                "Disease Duration (years)",
                0.0,
                100.0,
                5.0
            )

        with col3:

            severity = st.selectbox(
                "Disease Severity",
                [
                    "Mild",
                    "Moderate",
                    "Severe"
                ]
            )

            bmi = st.number_input(
                "BMI",
                0.0,
                100.0,
                25.0
            )

            hba1c = st.number_input(
                "HbA1c",
                0.0,
                30.0,
                7.5
            )


        st.subheader("Clinical Data")

        col1, col2, col3 = st.columns(3)

        with col1:

            systolic_bp = st.number_input(
                "Systolic BP",
                0.0,
                300.0,
                120.0
            )

            diastolic_bp = st.number_input(
                "Diastolic BP",
                0.0,
                200.0,
                80.0
            )

            fasting_glucose = st.number_input(
                "Fasting Glucose",
                0.0,
                1000.0,
                120.0
            )

        with col2:

            cholesterol = st.number_input(
                "Cholesterol",
                0.0,
                1000.0,
                180.0
            )

            kidney = st.selectbox(
                "Kidney Function",
                [
                    "Normal",
                    "Mild",
                    "Moderate",
                    "Severe"
                ]
            )

            liver = st.selectbox(
                "Liver Function",
                [
                    "Normal",
                    "Mild",
                    "Moderate",
                    "Severe"
                ]
            )

        with col3:

            smoking = st.selectbox(
                "Smoking Status",
                [
                    "Never",
                    "Former",
                    "Current"
                ]
            )

            alcohol = st.selectbox(
                "Alcohol Use",
                [
                    "None",
                    "Occasional",
                    "Regular"
                ]
            )

            pregnancy = st.selectbox(
                "Pregnancy Status",
                [
                    "Not Pregnant",
                    "Pregnant",
                    "Unknown"
                ]
            )


        st.subheader("Medical History")

        col1, col2 = st.columns(2)

        with col1:

            comorbidities = st.text_input(
                "Comorbidities",
                "None"
            )

            allergies = st.text_input(
                "Allergies",
                "None"
            )

        with col2:

            previous_treatment = st.text_input(
                "Previous Treatment",
                "None"
            )

            recent_surgery = st.selectbox(
                "Recent Surgery",
                [
                    "No",
                    "Yes"
                ]
            )


        serious_condition = st.selectbox(
            "Other Serious Condition",
            [
                "No",
                "Yes"
            ]
        )


        distance = st.number_input(
            "Distance From Trial Site (km)",
            0.0,
            10000.0,
            10.0
        )


        st.subheader("Recruitment")

        availability = st.selectbox(
            "Availability",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        contact_preference = st.selectbox(
            "Contact Preference",
            [
                "Phone",
                "Email",
                "SMS",
                "None"
            ]
        )

        consent = st.selectbox(
            "Consent To Contact",
            [
                "Yes",
                "No"
            ]
        )

        recruitment_status = st.selectbox(
            "Recruitment Status",
            [
                "Available",
                "Contacted",
                "Screening",
                "Enrolled",
                "Not Available"
            ]
        )


        submitted = st.form_submit_button(
            "➕ Add Patient",
            use_container_width=True
        )


    if submitted:

        if not patient_id.strip():

            st.error(
                "Patient ID is required."
            )

        else:

            patient = {

                "patient_id": patient_id.strip(),

                "age": age,

                "gender": gender,

                "location": location,

                "primary_disease": disease,

                "disease_duration_years": duration,

                "disease_severity": severity,

                "comorbidities": comorbidities,

                "previous_treatment": previous_treatment,

                "bmi": bmi,

                "systolic_bp": systolic_bp,

                "diastolic_bp": diastolic_bp,

                "hba1c": hba1c,

                "fasting_glucose": fasting_glucose,

                "kidney_function": kidney,

                "liver_function": liver,

                "cholesterol": cholesterol,

                "smoking_status": smoking,

                "alcohol_use": alcohol,

                "pregnancy_status": pregnancy,

                "allergies": allergies,

                "recent_surgery": recent_surgery,

                "other_serious_condition":
                    serious_condition,

                "distance_from_trial_site_km":
                    distance,

                "availability": availability,

                "contact_preference":
                    contact_preference,

                "consent_to_contact": consent,

                "recruitment_status":
                    recruitment_status,
            }


            try:

                add_patient(
                    patient
                )

                st.success(
                    f"Patient {patient_id} added successfully!"
                )

                st.info(
                    "The patient is now available "
                    "for trial matching."
                )

            except Exception as e:

                st.error(
                    f"Could not add patient: {e}"
                )


# ============================================================
# PATIENT DATABASE
# ============================================================

elif page == "👥 Patient Database":

    st.header(
        "👥 Live Patient Database"
    )

    st.metric(
        "Total Patients",
        len(patients)
    )

    search = st.text_input(
        "🔎 Search patient, disease or location"
    )


    if search:

        filtered = patients[
            patients.astype(str).apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

    else:

        filtered = patients


    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )