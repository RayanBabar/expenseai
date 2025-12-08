# ExpenseAI – API Reference

This document describes all available RESTful endpoints for the **ExpenseAI** backend system built for the UraanAI Techathon. The system supports user registration, government scheme verification, expense tracking, fraud detection, and AI chatbot integration.

All endpoints return JSON responses. The base URL during local development is:  
**`http://localhost:8000`**

---

## 🔐 1. User Registration

Registers a new user (employee, vendor, customer, or government official).

- **URL**: `/register`  
- **Method**: `POST`  
- **Request Body** (JSON):
  ```json
  {
    "cnic": "1234567890123",
    "name": "Ali Ahmed",
    "role": "employee",
    "spending_limit": 25000
  }
  ```
  - `role` must be one of: `"admin"`, `"employee"`, `"vendor"`, `"customer"`, `"government"`
  - `spending_limit` is required only for `"employee"`

- **Success Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "cnic": "1234567890123",
    "name": "Ali Ahmed",
    "role": "employee",
    "is_active": false
  }
  ```
  > ⚠️ Employee accounts start as **inactive**; admin must verify them before purchases.

- **Error Cases**:
  - `400 Bad Request`: Missing fields or invalid role
  - `400`: CNIC already exists

---

## 🔍 2. Verify Eligibility for Government Scheme

Checks if a citizen (by CNIC) qualifies for a welfare scheme using synthetic data.

- **URL**: `/verify`  
- **Method**: `POST`  
- **Request Body** (JSON):
  ```json
  {
    "cnic": "1234567890123",
    "scheme_id": "rashan_scheme"
  }
  ```
  - Valid `scheme_id`: `"rashan_scheme"`, `"scholarship_scheme"` (pre-seeded)

- **Success Response** (`200 OK`):
  ```json
  {
    "cnic": "1234567890123",
    "scheme_id": "rashan_scheme",
    "eligible": true,
    "trust_score": 85.5,
    "reasons": [],
    "government_recommendation": "ACCEPT"
  }
  ```
  - **eligible**: `true` or `false` (Predicted by Classifier).
  - **trust_score**: A float between `0.0` and `100.0` (Predicted by Regressor). Higher is better.
  - **reasons**: Explanations if the user is ineligible or has a low trust score (e.g., "History of defaults").
  - **government_recommendation**: Logic combines eligibility + trust score (e.g., must be Eligible AND Trust > 30).
- **Error Cases**:
  - `404 Not Found`: Invalid `scheme_id`

---

## 📤 3. Submit Government Decision & Trigger Expense

Government approves/rejects an application. If approved, ExpenseAI auto-generates an expense and invoice.

- **URL**: `/submit-proposal`  
- **Method**: `POST`  
- **Request Body** (JSON):
  ```json
  {
    "cnic": "1234567890123",
    "scheme_id": "rashan_scheme",
    "government_decision": "ACCEPTED"
  }
  ```
  - `government_decision` must be `"ACCEPTED"` or `"REJECTED"`

- **Success Response** (`200 OK`):
  - If **ACCEPTED**:
    ```json
    {
      "message": "Expense processed",
      "expense_id": "EXP8X3K9L2M",
      "fraud_flag": false
    }
    ```
  - If **REJECTED**:
    ```json
    {
      "message": "Proposal rejected"
    }
    ```

- **Side Effects**:
  - Creates an `Expense` record
  - Assigns a random vendor
  - Generates product list (e.g., wheat, rice)
  - Runs **fraud check** (e.g., flags if total > PKR 5,000)

---

## 📊 4. Get All Expense Records

Retrieves a list of all recorded expenses (for admin/government audit).

- **URL**: `/expenses`  
- **Method**: `GET`  
- **Request**: None  
- **Success Response** (`200 OK`):
  ```json
  [
    {
      "expense_id": "EXP8X3K9L2M",
      "cnic": "1234567890123",
      "scheme_id": "rashan_scheme",
      "vendor_cnic": "3456789012345",
      "total_amount": 2500.0,
      "products": "[{\"item\":\"Wheat Flour\",\"qty\":\"10kg\",\"price\":1500},...]",
      "is_fraudulent": false,
      "reason": null
    }
  ]
  ```

> 💡 `products` is a JSON-encoded string. Parse with `JSON.parse()` in frontend.

---

## 🤖 5. AI Chatbot (Urdu / English)

Stub endpoint for future NLP integration. Currently returns a demo response.

- **URL**: `/chatbot`  
- **Method**: `POST`  
- **Request Body** (JSON):
  ```json
  {
    "query": "Mera rashan kab milay ga?",
    "language": "ur"
  }
  ```
  - `language`: `"ur"` (Urdu) or `"en"` (English)

- **Success Response** (`200 OK`):
  ```json
  {
    "response": "Received your ur query: 'Mera rashan kab milay ga?'. This is a demo...",
    "detected_intent": "general_inquiry"
  }
  ```

> 🔜 In Phase 2, this will analyze fraud, spending patterns, or financial planning.

---

## ❤️ 6. Health Check

Verifies that the server and database are running.

- **URL**: `/health`  
- **Method**: `GET`  
- **Response** (`200 OK`):
  ```json
  {
    "status": "OK",
    "db": "connected"
  }
  ```

---

## 🧩 Notes on ML & Data

- **Synthetic Data Generation**: The system uses `train_models.py` to generate thousands of synthetic records (income, credit history, loan defaults) to train the models.
- **Deterministic Predictions**: During `/verify`, the user's profile is generated using their CNIC as a seed. This ensures that the same CNIC always yields the same synthetic financial profile and Trust Score, mimicking a real database lookup.
- **Trust Score Factors**: The score increases with paid utility bills and credit history, and decreases with loan defaults and suspicious transactions.

---

## 🔒 Security & Roles (Simplified)

| Role          | Can Register? | Can Verify? | Can Approve? | Can View Expenses? |
|---------------|---------------|-------------|--------------|---------------------|
| `government`  | ✅            | ✅          | ✅           | ✅                  |
| `admin`       | ✅            | ❌          | ❌           | ✅                  |
| `employee`    | ✅ (inactive) | ❌          | ❌           | ❌                  |
| `vendor`      | ✅            | ❌          | ❌           | ❌                  |
| `customer`    | ✅            | ❌          | ❌           | ❌                  |

> Full RBAC (Role-Based Access Control) can be added in Phase 2.

---

## 📎 Example Flow: Rashan Scheme

1. **Customer** registers as `role: "customer"`
2. **Government** calls `/verify` with CNIC and `scheme_id: "rashan_scheme"`
3. System returns `eligible: true`
4. **Government** calls `/submit-proposal` with `government_decision: "ACCEPTED"`
5. System:
   - Selects a vendor
   - Creates expense with food items
   - Flags fraud if needed
   - Logs invoice
6. **Admin** views `/expenses` to audit

---

✅ This API enables **transparent, traceable, and fraud-resistant** welfare distribution — fully aligned with UraanAI’s mission to reduce corruption in Pakistan.

---
