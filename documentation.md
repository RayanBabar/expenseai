# ExpenseAI – API Reference

This document describes all available RESTful endpoints for the **ExpenseAI** backend system built for the UraanAI Techathon. The system supports user registration, government scheme verification, identity checks, expense tracking, and AI chatbot integration.

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

-----

## 🔍 2. Verify Scheme Eligibility

Checks if a citizen (by CNIC) qualifies for a specific welfare scheme based on criteria (Income, Family Size) and AI predictions.

  - **URL**: `/verify-eligibility`

  - **Method**: `POST`

  - **Request Body** (JSON):

    ```json
    {
      "cnic": "1234567890123",
      "scheme_id": "rashan_scheme"
    }
    ```

      - Valid `scheme_id`: `"rashan_scheme"`, `"scholarship_scheme"`

  - **Success Response** (`200 OK`):

    ```json
    {
      "cnic": "1234567890123",
      "scheme_id": "rashan_scheme",
      "eligible": true,
      "reasons": []
    }
    ```

      - **eligible**: `true` or `false` (Based on AI Classifier + Scheme Rules).
      - **reasons**: Explanations if ineligible (e.g., "Income too high").

  - **Error Cases**:

      - `404 Not Found`: Invalid `scheme_id`

-----

## 🛡️ 3. Get Trust Score & Identity Verification

Verifies the user's identity (CNIC + Phone match) and calculates a financial Trust Score.

  - **URL**: `/trust-score`

  - **Method**: `POST`

  - **Request Body** (JSON):

    ```json
    {
      "cnic": "1234567890123",
      "phone_number": "03001234567"
    }
    ```

  - **Success Response** (`200 OK`):

    ```json
    {
      "cnic": "1234567890123",
      "phone_number": "03001234567",
      "is_identity_verified": true,
      "trust_score": 85.5,
      "reasons": []
    }
    ```

      - **is\_identity\_verified**: `true` if phone number is registered to the CNIC (Simulated NADRA/State Bank check).
      - **trust\_score**: Float `0.0` - `100.0` (Predicted by Regressor based on financial history).
      - **reasons**: Explanations for low score or failed verification (e.g., "Phone number mismatch", "History of defaults").

-----

## 📤 4. Submit Government Decision & Trigger Expense

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

-----

## 📊 5. Get All Expense Records

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

-----

## 🤖 6. AI Chatbot (Urdu / English)

Stub endpoint for future NLP integration.

  - **URL**: `/chatbot`

  - **Method**: `POST`

  - **Request Body** (JSON):

    ```json
    {
      "query": "Mera rashan kab milay ga?",
      "language": "ur"
    }
    ```

  - **Success Response** (`200 OK`):

    ```json
    {
      "response": "Received your ur query...",
      "detected_intent": "general_inquiry"
    }
    ```

-----

## ❤️ 7. Health Check

  - **URL**: `/health`
  - **Method**: `GET`
  - **Response** (`200 OK`):
    ```json
    {
      "status": "OK",
      "db": "connected"
    }
    ```
