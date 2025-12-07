# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import random
import string

from src.database import get_db
from src.models import User, Scheme, Application, Expense
from src.schemas import UserCreate, UserOut, VerifyEligibilityRequest, VerifyEligibilityResponse, SubmitProposalRequest, ExpenseRecord, ChatbotQuery
from src.crud import verify_eligibility, create_application, create_expense_record

app = FastAPI(title="ExpenseAI - UraanAI Techathon", version="1.0")

# Initialize synthetic schemes on first run
@app.on_event("startup")
def init_schemes_and_vendors():
    db = next(get_db())
    
    # Seed schemes
    if db.query(Scheme).count() == 0:
        schemes = [
            Scheme(scheme_id="rashan_scheme", name="Rashan Scheme", description="Food support", max_income=50000, min_family_size=3),
            Scheme(scheme_id="scholarship_scheme", name="Scholarship", description="Education aid", max_income=70000)
        ]
        db.add_all(schemes)
        db.commit()

    # Seed a default vendor
    if db.query(User).filter(User.role == "vendor").count() == 0:
        default_vendor = User(
            cnic="9999999999999",
            name="Default Rashan Vendor",
            role="vendor",
            is_active=True
        )
        db.add(default_vendor)
        db.commit()

# --- User Registration ---
@app.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.cnic == user.cnic).first()
    if db_user:
        raise HTTPException(status_code=400, detail="CNIC already registered")
    new_user = User(
        cnic=user.cnic,
        name=user.name,
        role=user.role,
        is_active=(user.role == "government"),  # Gov auto-active; others need approval
        spending_limit=user.spending_limit
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- Eligibility Verification ---
@app.post("/verify", response_model=VerifyEligibilityResponse)
def verify_eligibility_endpoint(request: VerifyEligibilityRequest, db: Session = Depends(get_db)):
    eligible, trust_score, reasons = verify_eligibility(db, request.cnic, request.scheme_id)
    
    if eligible is None:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    create_application(db, request.cnic, request.scheme_id, eligible)
    
    return VerifyEligibilityResponse(
        cnic=request.cnic,
        scheme_id=request.scheme_id,
        eligible=eligible,
        trust_score=round(trust_score, 1), # Round for cleaner API output
        reasons=reasons,
        government_recommendation="ACCEPT" if eligible and trust_score > 30 else "REJECT"
    )

# --- Submit Government Decision & Trigger Expense ---
@app.post("/submit-proposal")
def submit_proposal(request: SubmitProposalRequest, db: Session = Depends(get_db)):
    app = db.query(Application).filter(
        Application.cnic == request.cnic,
        Application.scheme_id == request.scheme_id
    ).order_by(Application.created_at.desc()).first()
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    app.government_decision = request.government_decision
    db.commit()

    if request.government_decision == "ACCEPTED":
        # Simulate vendor selection
        vendors = db.query(User).filter(User.role == "vendor").all()
        if not vendors:
            raise HTTPException(status_code=500, detail="No vendors available")
        vendor = random.choice(vendors)

        # Simulate products
        products = [
            {"item": "Wheat Flour", "qty": "10kg", "price": 1500},
            {"item": "Rice", "qty": "5kg", "price": 1000}
        ]
        total = sum(p["price"] for p in products)

        # Fraud check (simplified)
        is_fraud = total > 5000  # Example rule
        reason = "Excessive amount" if is_fraud else None

        expense_id = "EXP" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expense_data = {
            "expense_id": expense_id,
            "cnic": request.cnic,
            "scheme_id": request.scheme_id,
            "vendor_cnic": vendor.cnic,
            "total_amount": total,
            "products": json.dumps(products),
            "is_fraudulent": is_fraud,
            "reason": reason
        }
        create_expense_record(db, expense_data)
        return {"message": "Expense processed", "expense_id": expense_id, "fraud_flag": is_fraud}
    else:
        return {"message": "Proposal rejected"}

# --- Get All Expenses ---
@app.get("/expenses", response_model=List[ExpenseRecord])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()
    return [ExpenseRecord(
        expense_id=e.expense_id,
        cnic=e.cnic,
        scheme_id=e.scheme_id,
        vendor_cnic=e.vendor_cnic,
        total_amount=e.total_amount,
        products=e.products,
        is_fraudulent=e.is_fraudulent,
        reason=e.reason
    ) for e in expenses]

# --- AI Chatbot Stub (Urdu/English) ---
@app.post("/chatbot")
def chatbot(query: ChatbotQuery):
    # In Phase-2: integrate NLP model
    return {
        "response": f"Received your {query.language} query: '{query.query}'. This is a demo. In production, AI would analyze fraud, purchases, or planning.",
        "detected_intent": "general_inquiry"
    }

@app.get("/health")
def health():
    return {"status": "OK", "db": "connected"}