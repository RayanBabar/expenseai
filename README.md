# ExpenseAI - AI-Powered Government Expense Verification & Fraud Detection System

**For UraanAI Techathon – Pakistan**

ExpenseAI is a transparent, AI-assisted platform designed to reduce corruption in government welfare schemes by automating eligibility verification, expense tracking, and fraud detection. Unlike traditional rule-based systems, ExpenseAI utilizes **Machine Learning models** to predict beneficiary eligibility and assign a **Trust Score** based on financial history and behavioral patterns.

Built with **FastAPI (Python)**, **Scikit-Learn**, and **SQLite**, this backend supports role-based portals for **Government**, **Vendors**, **Employees**, and **Local Customers**, and includes a foundation for an **AI Chatbot (Urdu/English)**.

---

## 🌟 Core Features

- ✅ **ML-Powered Eligibility Verification**: A trained Classifier predicts eligibility based on income, family size, and utility bill history (replacing static rules).
- ✅ **Identity & Trust Scoring**: 
  - **Identity Check**: Verifies if the applicant's phone number matches their CNIC (Simulated State Bank/NADRA check).
  - **Trust Score**: A Regressor model assigns a **Score (0-100)** based on credit history, loan defaults, and transaction patterns.
- ✅ **Government Scheme Management**: Pre-configured schemes (e.g., Rashan, Scholarships) with customizable parameters.
- ✅ **Expense Tracking & Invoicing**: Auto-generates invoices upon government approval; logs all transactions.
- ✅ **Fraud Detection**: Flags fake purchases, excessive spending, or policy violations.
- ✅ **Role-Based Access**:
  - `government`: Approve/reject applications & view Trust Scores.
  - `vendor`: Fulfill orders, receive payments.
  - `employee`: Make purchases (within limits).
  - `customer`: Receive benefits.
- ✅ **100% Synthetic Data Pipeline**: Includes a training script that generates realistic synthetic data to train the AI models locally.

---

## 🗃️ Database Schema (SQLite)

| Table        | Description |
|--------------|-------------|
| `users`      | Stores CNIC, name, role, spending limits |
| `schemes`    | Government welfare programs with eligibility rules |
| `applications` | Records eligibility checks, **Trust Scores**, and decisions |
| `expenses`   | Tracks all purchases, vendor info, fraud flags, and receipts |

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI/ML**: Scikit-Learn, Pandas, NumPy, Joblib
- **Database**: SQLite (file-based)
- **Package Manager**: `uv` (Astral)
- **Deployment Ready**: Can be containerized or run locally

---

## 📁 Project Structure
```
expenseai/
├── main.py \# FastAPI app entrypoint
├── train\_models.py \# Script to generate synthetic data & train ML models
├── synthetic\_data.csv \# Generated dataset for training
├── results/ \# Stores evaluation graphs (Confusion Matrix, Metrics)
├── src
    ├── models.py \# SQLAlchemy data models
    ├── database.py \# DB engine & session setup
    ├── schemas.py \# Pydantic request/response models
    ├── crud.py \# Business logic (Loads ML models for inference)
    ├── eligibility\_model.pkl \# Trained Classifier
    ├── trust\_model.pkl \# Trained Regressor
├── expenseai.db \# Auto-generated SQLite database
├── README.md
├── documentation.md
└── instructions.md
```

---

## 📜 License

This project is open-source and intended for educational and competition use (UraanAI Techathon 2025). MIT License.
