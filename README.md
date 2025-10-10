# ExpenseAI – AI-Powered Government Expense Verification & Fraud Detection System

**For UraanAI Techathon – Pakistan**

ExpenseAI is a transparent, AI-assisted platform designed to reduce corruption in government welfare schemes by automating eligibility verification, expense tracking, and fraud detection using synthetic data and secure record-keeping. It ensures subsidies like the **Rashan Scheme** reach only deserving beneficiaries through biometric-verified, traceable transactions.

Built with **FastAPI (Python)** and **SQLite**, this backend supports role-based portals for **Government**, **Vendors**, **Employees**, and **Local Customers**, and includes a foundation for an **AI Chatbot (Urdu/English)** for user interaction and fraud alerts.

---

## 🌟 Core Features

- ✅ **Automated Eligibility Verification**: Uses synthetic NADRA/WAPDA-like data to assess income, family size, and utility payment history.
- ✅ **Government Scheme Management**: Pre-configured schemes (e.g., Rashan, Scholarships) with customizable rules.
- ✅ **Expense Tracking & Invoicing**: Auto-generates invoices upon government approval; logs all transactions.
- ✅ **Fraud Detection**: Flags fake purchases, excessive spending, or policy violations.
- ✅ **Role-Based Access**:
  - `government`: Approve/reject applications
  - `vendor`: Fulfill orders, receive payments
  - `employee`: Make purchases (within limits)
  - `customer`: Receive benefits
- ✅ **AI Chatbot Ready**: Endpoints prepared for Urdu/English NLP integration (Phase 2).
- ✅ **100% Synthetic Data**: No real government APIs used — fully compliant with UraanAI Phase-1 rules.

---

## 🗃️ Database Schema (SQLite)

| Table        | Description |
|--------------|-------------|
| `users`      | Stores CNIC, name, role, spending limits |
| `schemes`    | Government welfare programs with eligibility rules |
| `applications` | Records eligibility checks and government decisions |
| `expenses`   | Tracks all purchases, vendor info, fraud flags, and receipts |

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (file-based, no setup needed)
- **Authentication**: Role-based (simplified for demo)
- **Deployment Ready**: Can be containerized or run locally

---

## 📁 Project Structure

```
expenseai/
├── main.py          # FastAPI app entrypoint
├── src    
    ├── models.py        # SQLAlchemy data models
    ├── database.py      # DB engine & session setup
    ├── schemas.py       # Pydantic request/response models
    ├── crud.py          # Business logic (eligibility, fraud checks)
├── expenseai.db     # Auto-generated SQLite database
├── README.md
├── documentation.md
└── instructions.md
```

---

## 📜 License

This project is open-source and intended for educational and competition use (UraanAI Techathon 2025). MIT License.

---