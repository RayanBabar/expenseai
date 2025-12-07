# src/crud.py
import random
import os
import joblib
import pandas as pd
from sqlalchemy.orm import Session
from . import models

# --- Load ML Model Globaly ---
# We load this at the top level so we don't reload it for every request.
MODEL_PATH = os.path.join(os.path.dirname(__file__), "eligibility_model.pkl")
ML_MODEL = None

try:
    if os.path.exists(MODEL_PATH):
        ML_MODEL = joblib.load(MODEL_PATH)
        print(f"ML Model loaded successfully from {MODEL_PATH}")
    else:
        print("Warning: eligibility_model.pkl not found. Run train_model.py first.")
except Exception as e:
    print(f"Error loading ML model: {e}")


# Synthetic data generator (simulates NADRA/WAPDA/etc.)
def get_synthetic_profile(cnic: str):
    # In real system: call NADRA API
    return {
        "income": random.choice([30000, 45000, 60000, 80000]),
        "family_size": random.randint(2, 6),
        "utility_bills_paid": random.choice([True, True, False])
    }

def verify_eligibility(db: Session, cnic: str, scheme_id: str):
    # 1. Check if scheme exists
    scheme = db.query(models.Scheme).filter(models.Scheme.scheme_id == scheme_id).first()
    if not scheme:
        return None, ["Scheme not found"]

    # 2. Get Citizen Profile (Synthetic Data)
    profile = get_synthetic_profile(cnic)
    reasons = []
    eligible = False

    # 3. Use ML Model if available
    if ML_MODEL:
        # Prepare input dataframe for the model
        # Note: We convert utility_bills_paid to 1 or 0 to match training data
        input_features = pd.DataFrame([{
            "income": profile["income"],
            "family_size": profile["family_size"],
            "utility_bills_paid": 1 if profile["utility_bills_paid"] else 0
        }])

        # Predict (returns array, take first element)
        prediction = ML_MODEL.predict(input_features)[0]
        eligible = bool(prediction)

        if not eligible:
            # Since ML models are "black boxes", we infer reasons or give a generic message.
            # Ideally, you'd use SHAP values here for explainability, but for now:
            reasons.append(f"AI Model determined ineligibility based on profile: "
                           f"Income={profile['income']}, Family={profile['family_size']}")
            if not profile["utility_bills_paid"]:
                reasons.append("Historical data indicates unpaid utility bills reduce score.")

    else:
        # --- Fallback to Rule-Based (if model is missing) ---
        eligible = True
        if profile["income"] > scheme.max_income:
            eligible = False
            reasons.append(f"Income {profile['income']} > limit {scheme.max_income}")
        if profile["family_size"] < scheme.min_family_size:
            eligible = False
            reasons.append(f"Family size {profile['family_size']} < min {scheme.min_family_size}")
        if not profile["utility_bills_paid"]:
            eligible = False
            reasons.append("Utility bills unpaid")

    return eligible, reasons

def create_application(db: Session, cnic: str, scheme_id: str, eligible: bool):
    app = models.Application(cnic=cnic, scheme_id=scheme_id, eligible=eligible)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

def create_expense_record(db: Session, expense_data: dict):
    expense = models.Expense(**expense_data)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense