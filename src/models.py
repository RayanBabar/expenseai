# models.py
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    cnic = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=False)
    spending_limit = Column(Float, nullable=True)

class Scheme(Base):
    __tablename__ = "schemes"
    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    max_income = Column(Float)
    min_family_size = Column(Integer, default=0)

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    cnic = Column(String, index=True)
    scheme_id = Column(String, index=True)
    eligible = Column(Boolean)
    government_decision = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(String, unique=True, index=True)
    cnic = Column(String, index=True)
    scheme_id = Column(String, index=True)
    vendor_cnic = Column(String)
    total_amount = Column(Float)
    products = Column(String)
    is_fraudulent = Column(Boolean, default=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)