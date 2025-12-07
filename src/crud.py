# src/crud.py
import random
import os
import joblib
import pandas as pd
from sqlalchemy.orm import Session
from . import models

# --- Load Models ---
BASE_DIR = os.path.dirname(__file__)
ELIGIBILITY_MODEL_PATH = os.path.join(BASE_DIR, "eligibility_model.pkl")
TRUST_MODEL_PATH = os.path.join(BASE_DIR, "trust_model.pkl")

ELIGIBILITY_MODEL = None
TRUST_MODEL = None

try:
    if os.path.exists(ELIGIBILITY_MODEL_PATH):
        ELIGIBILITY_MODEL = joblib.load(ELIGIBILITY_MODEL_PATH)
        print("Loaded Eligibility Model")
    if os.path.exists(TRUST_MODEL_PATH):
        TRUST_MODEL = joblib.load(TRUST_MODEL_PATH)
        print("Loaded Trust Model")
except Exception as e:
    print(f"Error loading models: {e}")

# Synthetic data generator
def get_synthetic_profile(cnic: str):
    # Use CNIC as seed so the same user always gets the same 'random' data
    # This ensures "prediction based on user cnic" is consistent.
    random.seed(cnic)
    
    return {
        "income": random.choice([30000, 45000, 60000, 80000, 120000]),
        "family_size": random.randint(2, 8),
        "utility_bills_paid": random.choice([True, True, False]),
        "loan_defaults": random.choice([0, 0, 0, 0, 1]), # 20% chance
        "credit_history_years": random.randint(0, 15),
        "suspicious_transactions": random.choice([0, 0, 0, 1, 2])
    }

def verify_eligibility(db: Session, cnic: str, scheme_id: str):
    scheme = db.query(models.Scheme).filter(models.Scheme.scheme_id == scheme_id).first()
    if not scheme:
        return None, 0.0, ["Scheme not found"] # Added 0.0 for trust score return signature

    profile = get_synthetic_profile(cnic)
    reasons = []
    eligible = False
    trust_score = 50.0 # Default neutral score

    # 1. Predict Eligibility
    if ELIGIBILITY_MODEL:
        features_cls = pd.DataFrame([{
            "income": profile["income"],
            "family_size": profile["family_size"],
            "utility_bills_paid": 1 if profile["utility_bills_paid"] else 0
        }])
        eligible = bool(ELIGIBILITY_MODEL.predict(features_cls)[0])
        
        if not eligible:
            reasons.append("AI Model predicted ineligibility based on financial profile.")
    else:
        # Fallback Rules
        eligible = True
        if profile["income"] > scheme.max_income:
            eligible = False
            reasons.append("Income too high")
        if not profile["utility_bills_paid"]:
            eligible = False
            reasons.append("Utility bills unpaid")

    # 2. Predict Trust Score
    if TRUST_MODEL:
        features_reg = pd.DataFrame([{
            "income": profile["income"],
            "family_size": profile["family_size"],
            "utility_bills_paid": 1 if profile["utility_bills_paid"] else 0,
            "loan_defaults": profile["loan_defaults"],
            "credit_history_years": profile["credit_history_years"],
            "suspicious_transactions": profile["suspicious_transactions"]
        }])
        trust_score = float(TRUST_MODEL.predict(features_reg)[0])
        
        # Add explanation for low trust
        if trust_score < 40:
            reasons.append(f"Low Trust Score ({trust_score:.1f}): History of defaults or suspicious activity detected.")
    
    return eligible, trust_score, reasons

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