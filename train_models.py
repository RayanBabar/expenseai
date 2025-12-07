# train_model.py
import pandas as pd
import random
import os
import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, f1_score, classification_report, ConfusionMatrixDisplay,
    mean_absolute_error, r2_score
)

random.seed(42)
os.environ['PYTHONHASHSEED'] = '42'

# --- 1. Synthetic Data Generation ---
def generate_synthetic_data(num_samples=10000):
    data = []
    print(f"Generating {num_samples} synthetic records...")
    
    for _ in range(num_samples):
        # -- Features --
        income = random.randint(20000, 100000)
        family_size = random.randint(1, 10)
        utility_bills_paid = random.choice([0, 1]) 
        
        # New Features for Trust Score
        loan_defaults = random.choice([0, 0, 0, 1]) # 25% chance of default
        credit_history_years = random.randint(0, 20)
        suspicious_transactions = random.randint(0, 5)

        # -- Ground Truth Logic: Eligibility (Classification) --
        is_eligible = 0
        if utility_bills_paid == 1:
            if income <= 50000:
                is_eligible = 1
            elif income <= 70000 and family_size >= 4:
                is_eligible = 1
        
        # -- Ground Truth Logic: Trust Score (Regression 0-100) --
        # Base score 50
        score = 50 
        score += (utility_bills_paid * 20)      # +20 if bills paid
        score += (credit_history_years * 1.5)   # +1.5 per year of history
        score -= (loan_defaults * 30)           # -30 if defaulted
        score -= (suspicious_transactions * 10) # -10 per suspicious txn
        score += (income / 5000)                # Slight boost from income
        
        # Clamp between 0 and 100
        score = max(0, min(100, score))
        # Add some random noise to make it realistic for ML
        score += random.randint(-5, 5)
        score = max(0, min(100, score))

        data.append([
            income, family_size, utility_bills_paid, 
            loan_defaults, credit_history_years, suspicious_transactions,
            is_eligible, score
        ])

    columns = [
        'income', 'family_size', 'utility_bills_paid', 
        'loan_defaults', 'credit_history_years', 'suspicious_transactions',
        'is_eligible', 'trust_score'
    ]
    return pd.DataFrame(data, columns=columns)

def train():
    df = generate_synthetic_data()
    df.to_csv("synthetic_data.csv", index=False)
    print("Synthetic data saved to synthetic_data.csv")
    
    os.makedirs("results/eligibility_model", exist_ok=True)
    os.makedirs("results/trust_model", exist_ok=True)
    
    # Create src directory
    if not os.path.exists("src"):
        os.makedirs("src")

    # ==========================================
    # MODEL 1: Eligibility Classifier
    # ==========================================
    print("\n--- Training Eligibility Model (Classifier) ---")
    X_cls = df[['income', 'family_size', 'utility_bills_paid']]
    y_cls = df['is_eligible']
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)
    
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_train_c, y_train_c)
    
    # Evaluation
    y_pred_c = clf.predict(X_test_c)
    acc = accuracy_score(y_test_c, y_pred_c)
    f1 = f1_score(y_test_c, y_pred_c)
    print(f"Accuracy: {acc:.2%}, F1: {f1:.2f}")

    # Save Classifier
    joblib.dump(clf, "src/eligibility_model.pkl")

    # Graph: Confusion Matrix
    plt.figure(figsize=(6, 5))
    ConfusionMatrixDisplay.from_estimator(clf, X_test_c, y_test_c, cmap=plt.cm.Blues)
    plt.title("Eligibility Confusion Matrix")
    plt.savefig(os.path.join("results/eligibility_model", "confusion_matrix.png"))
    plt.close()
    
    # Calculate and Save Classification Report(f1, recall, precision, accuracy) as bar chart
    report = classification_report(y_test_c, y_pred_c, output_dict=True)
    metrics = ['precision', 'recall', 'f1-score']
    labels = ['0', '1']
    x = np.arange(len(labels))
    width = 0.2
    plt.figure(figsize=(8, 6))
    for i, metric in enumerate(metrics):
        values = [report[label][metric] for label in labels]
        plt.bar(x + i*width, values, width, label=metric)
    
    # Add accuracy as a horizontal line
    plt.axhline(y=acc, color='red', linestyle='--', linewidth=2, label=f'Accuracy: {acc:.2f}')
    
    plt.xlabel("Classes")
    plt.ylabel("Scores")
    plt.title("Classification Report Metrics")
    plt.xticks(x + width, labels)
    plt.ylim(0, 1)
    plt.legend()
    plt.savefig(os.path.join("results/eligibility_model", "classification_report.png"))
    plt.close()

    # ==========================================
    # MODEL 2: Trust Score Regressor
    # ==========================================
    print("\n--- Training Trust Model (Regressor) ---")
    # Using more features for trust
    features_trust = [
        'income', 'family_size', 'utility_bills_paid', 
        'loan_defaults', 'credit_history_years', 'suspicious_transactions'
    ]
    X_reg = df[features_trust]
    y_reg = df['trust_score']

    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train_r, y_train_r)

    # Evaluation
    y_pred_r = reg.predict(X_test_r)
    mae = mean_absolute_error(y_test_r, y_pred_r)
    r2 = r2_score(y_test_r, y_pred_r)
    print(f"Mean Absolute Error: {mae:.2f} points")
    print(f"R2 Score: {r2:.2f}")

    # Save Regressor
    joblib.dump(reg, "src/trust_model.pkl")

    # Graph: Actual vs Predicted Trust Scores
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test_r, y_pred_r, alpha=0.3, color='purple')
    plt.plot([0, 100], [0, 100], color='red', linestyle='--') # Ideal line
    plt.xlabel("Actual Trust Score")
    plt.ylabel("Predicted Trust Score")
    plt.title(f"Trust Score Prediction (MAE: {mae:.2f})")
    plt.grid(True)
    plt.savefig(os.path.join("results/trust_model", "actual_vs_predicted.png"))
    plt.close()

    print("\nTraining complete. Models and graphs saved.")

if __name__ == "__main__":
    train()