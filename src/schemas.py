# schemas.py
from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    cnic: str
    name: str
    role: str  # 'admin', 'employee', 'vendor', 'customer', 'government'
    spending_limit: Optional[float] = None

class UserOut(BaseModel):
    id: int
    cnic: str
    name: str
    role: str
    is_active: bool

class VerifyEligibilityRequest(BaseModel):
    cnic: str
    scheme_id: str

class VerifyEligibilityResponse(BaseModel):
    cnic: str
    scheme_id: str
    eligible: bool
    reasons: List[str]
    government_recommendation: str

class SubmitProposalRequest(BaseModel):
    cnic: str
    scheme_id: str
    government_decision: str  # "ACCEPTED" or "REJECTED"

class ExpenseRecord(BaseModel):
    expense_id: str
    cnic: str
    scheme_id: str
    vendor_cnic: str
    total_amount: float
    products: str  # JSON string
    is_fraudulent: bool
    reason: Optional[str]

class ChatbotQuery(BaseModel):
    query: str
    language: str  # "ur" or "en"