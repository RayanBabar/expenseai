# 🚀 Instructions to Run ExpenseAI Backend & Integrate with Flutter

This guide explains how to:
1. Set up and run the **FastAPI backend** using `uv`
2. Connect a **Flutter frontend** to the API

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

---

## ▶️ Step 2: Install Dependencies with `uv`

```bash
# Create virtual environment & install deps
uv sync
```

> ✅ This uses `uv` for faster, reliable dependency resolution.

---

## ▶️ Step 3: Run the FastAPI Server

```bash
uv run -- uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- The API will be live at: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`

> 💡 On first run, the system auto-creates `expenseai.db` and seeds sample schemes.

---

## 📲 Step 4: Integrate with Flutter Frontend

### A. Add Internet Permission (Android)

In `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### B. Add HTTP Client (Dart)

Use the `http` package:

```yaml
# pubspec.yaml
dependencies:
  http: ^0.15.0
```

### C. Example: Verify Eligibility from Flutter

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<void> verifyEligibility(String cnic, String schemeId) async {
  final url = Uri.parse('http://10.0.2.2:8000/verify'); // Android emulator
  // For physical device or iOS: use your machine's IP (e.g., 192.168.x.x)

  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'cnic': cnic,
      'scheme_id': schemeId,
    }),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    print('Eligible: ${data['eligible']}');
  } else {
    print('Error: ${response.body}');
  }
}
```

### 🔁 Replace `10.0.2.2` with your **local IP** if testing on a real device:
```bash
ipconfig  # Windows
ifconfig   # Mac/Linux
```

### D. Key API Endpoints for Flutter

| Purpose                     | Method | Endpoint               | Body Example |
|----------------------------|--------|------------------------|--------------|
| Register User              | POST   | `/register`            | `{"cnic":"...","name":"...","role":"customer"}` |
| Verify Eligibility         | POST   | `/verify`              | `{"cnic":"...","scheme_id":"rashan_scheme"}` |
| Submit Govt Decision       | POST   | `/submit-proposal`     | `{"cnic":"...","scheme_id":"...","government_decision":"ACCEPTED"}` |
| Get All Expenses           | GET    | `/expenses`            | — |
| Chatbot Query (Demo)       | POST   | `/chatbot`             | `{"query":"Rashan status?","language":"ur"}` |

---

## 🌐 Network Notes

- **Emulator**: Use `10.0.2.2:8000`
- **Physical Device**: Use your computer’s **local IP** (e.g., `192.168.1.10:8000`)
- Ensure your **firewall allows port 8000**

---

## 🧪 Testing

Use **Postman** or **Swagger UI** (`/docs`) to test APIs before connecting Flutter.

---
