# 🚀 Instructions to Run ExpenseAI Backend & Integrate with Flutter

This guide explains how to:
1. Set up and run the **FastAPI backend**
2. **Train the AI Models** locally
3. Connect a **Flutter frontend** to the API

---

## 🧰 Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- [`uv` (Ultra-fast Python package installer)](https://docs.astral.sh/uv/)
- Flutter SDK (for frontend integration)

---

## ▶️ Step 1: Clone & Set Up Backend

```bash
git clone https://github.com/RayanBabar/expenseai.git
cd expenseai
```

-----

## ▶️ Step 2: Install Dependencies with `uv`

```bash
# Create virtual environment & install deps (including scikit-learn, pandas)
uv sync
```

-----

## ▶️ Step 3: Train AI Models (Crucial Step)

Before running the server, you must generate the synthetic data and train the machine learning models. This creates the `.pkl` files needed for the API.

```bash
uv run python train_models.py
```

> **Output**: This will save `eligibility_model.pkl` and `trust_model.pkl` in the `src/` folder and generate performance graphs in the `results/` folder.

-----

## ▶️ Step 4: Run the FastAPI Server

```bash
uv run -- uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

  - The API will be live at: `http://localhost:8000`
  - Interactive docs (Swagger UI): `http://localhost:8000/docs`

> 💡 The server loads the trained models on startup to perform real-time inference.

-----

## 📲 Step 5: Integrate with Flutter Frontend

### A. Add Internet Permission (Android)

In `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### B. Add HTTP Client (Dart)

```yaml
# pubspec.yaml
dependencies:
  http: ^0.15.0
```

### C. Example: Verify Eligibility & Check Trust

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

// 1. Check Scheme Eligibility
Future<void> checkEligibility(String cnic, String schemeId) async {
  final url = Uri.parse('http://10.0.2.2:8000/verify-eligibility');
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'cnic': cnic, 'scheme_id': schemeId}),
  );

  if (response.statusCode == 200) {
    print('Eligibility: ${jsonDecode(response.body)}');
  }
}

// 2. Check Identity & Trust Score
Future<void> checkTrustScore(String cnic, String phoneNumber) async {
  final url = Uri.parse('http://10.0.2.2:8000/trust-score');
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'cnic': cnic, 'phone_number': phoneNumber}),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    print('Identity Verified: ${data['is_identity_verified']}');
    print('Trust Score: ${data['trust_score']}');
  }
}
```

### D. Key API Endpoints for Flutter

| Purpose                     | Method | Endpoint               | Response Includes |
|----------------------------|--------|------------------------|-------------------|
| Register User              | POST   | `/register`            | User details |
| **Verify Eligibility** | POST   | `/verify-eligibility`  | `eligible` (bool), `reasons` |
| **Get Trust Score** | POST   | `/trust-score`         | `trust_score`, `is_identity_verified` |
| Submit Govt Decision       | POST   | `/submit-proposal`     | Status, Expense ID |
| Get All Expenses           | GET    | `/expenses`            | List of expenses |
| Chatbot Query              | POST   | `/chatbot`             | AI response |

-----

## 🌐 Network Notes

  - **Emulator**: Use `10.0.2.2:8000`
  - **Physical Device**: Use your computer’s **local IP** (e.g., `192.168.1.10:8000`)
  - Ensure your **firewall allows port 8000**.
