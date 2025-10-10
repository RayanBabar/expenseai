# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

SQLITE_FILE = "expenseai.db"
engine = create_engine(f"sqlite:///{SQLITE_FILE}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()