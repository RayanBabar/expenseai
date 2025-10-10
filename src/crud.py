# crud.py
import random
from sqlalchemy.orm import Session
from . import models

# Synthetic data generator (simulates NADRA/WAPDA/etc.)
def get_synthetic_profile(cnic: str):
    # In real system: call NADRA API
    return {
        "income": random.choice([30000, 45000, 60000, 80000]),
        "family_size": random.randint(2, 6),
        "utility_bills_paid": random.choice([True, True, False])
    }

def verify_eligibility(db: Session, cnic: str, scheme_id: str):
    scheme = db.query(models.Scheme).filter(models.Scheme.scheme_id == scheme_id).first()
    if not scheme:
        return None, ["Scheme not found"]

    profile = get_synthetic_profile(cnic)
    reasons = []
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