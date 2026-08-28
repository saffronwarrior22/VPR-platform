import sqlite3
import pandas as pd


DB_NAME = "patients.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return sqlite3.connect(DB_NAME)


# ============================================================
# CREATE TABLE
# ============================================================

def initialize_database():

    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            age REAL,
            gender TEXT,
            location TEXT,
            primary_disease TEXT,
            disease_duration_years REAL,
            disease_severity TEXT,
            comorbidities TEXT,
            previous_treatment TEXT,
            bmi REAL,
            systolic_bp REAL,
            diastolic_bp REAL,
            hba1c REAL,
            fasting_glucose REAL,
            kidney_function TEXT,
            liver_function TEXT,
            cholesterol REAL,
            smoking_status TEXT,
            alcohol_use TEXT,
            pregnancy_status TEXT,
            allergies TEXT,
            recent_surgery TEXT,
            other_serious_condition TEXT,
            distance_from_trial_site_km REAL,
            availability TEXT,
            contact_preference TEXT,
            consent_to_contact TEXT,
            recruitment_status TEXT
        )
        """
    )

    conn.commit()
    conn.close()


# ============================================================
# IMPORT EXISTING CSV
# ============================================================

def import_csv_if_empty(csv_file):

    conn = get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]

    conn.close()

    # Don't import again if database already contains patients.
    if count > 0:
        return

    df = pd.read_csv(csv_file)

    conn = get_connection()

    df.to_sql(
        "patients",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()


# ============================================================
# LOAD ALL PATIENTS
# ============================================================

def load_patients():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM patients",
        conn
    )

    conn.close()

    return df


# ============================================================
# ADD PATIENT
# ============================================================

def add_patient(patient):

    conn = get_connection()

    columns = list(patient.keys())

    placeholders = ",".join(
        ["?"] * len(columns)
    )

    column_names = ",".join(columns)

    query = f"""
        INSERT INTO patients
        ({column_names})
        VALUES
        ({placeholders})
    """

    conn.execute(
        query,
        list(patient.values())
    )

    conn.commit()
    conn.close()


# ============================================================
# UPDATE PATIENT
# ============================================================

def update_patient(patient_id, updates):

    conn = get_connection()

    set_clause = ", ".join(
        [f"{key} = ?" for key in updates]
    )

    query = f"""
        UPDATE patients
        SET {set_clause}
        WHERE patient_id = ?
    """

    conn.execute(
        query,
        list(updates.values()) + [patient_id]
    )

    conn.commit()
    conn.close()


# ============================================================
# SEARCH PATIENTS
# ============================================================

def search_patients(search_text):

    conn = get_connection()

    query = """
        SELECT *
        FROM patients
        WHERE patient_id LIKE ?
        OR primary_disease LIKE ?
        OR location LIKE ?
    """

    pattern = f"%{search_text}%"

    df = pd.read_sql_query(
        query,
        conn,
        params=[
            pattern,
            pattern,
            pattern
        ]
    )

    conn.close()

    return df


# ============================================================
# PATIENT COUNT
# ============================================================

def patient_count():

    conn = get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]

    conn.close()

    return count