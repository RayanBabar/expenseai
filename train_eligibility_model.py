import pandas as pd
import random
import os
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, 
    f1_score, 
    recall_score, 
    precision_score, 
    confusion_matrix, 
    ConfusionMatrixDisplay
)

random.seed(42)
os.environ['PYTHONHASHSEED'] = '42'

def generate_synthetic_data(num_samples=10000):
    data = []
    print(f"Generating {num_samples} synthetic records...")
    
    for _ in range(num_samples):
        # 1. Generate Features
        income = random.randint(20000, 100000)
        family_size = random.randint(1, 10)
        utility_bills_paid = random.choice([0, 1]) 
        
        # 2. Define "Ground Truth" Logic
        # Rule: Eligible (1) if (Income < 50k) OR (Income < 70k AND Family Size > 4)
        # AND Utility bills must be paid.
        is_eligible = 0
        
        if utility_bills_paid == 1:
            if income <= 50000:
                is_eligible = 1
            elif income <= 70000 and family_size >= 4:
                is_eligible = 1
        
        data.append([income, family_size, utility_bills_paid, is_eligible])

    return pd.DataFrame(data, columns=['income', 'family_size', 'utility_bills_paid', 'target'])

def train():
    
    os.makedirs("results/eligibility_model", exist_ok=True)
    
    # --- 1. Data Prep ---
    df = generate_synthetic_data()
    df.to_csv("synthetic_data.csv", index=False)
    
    X = df[['income', 'family_size', 'utility_bills_paid']]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- 2. Train Model ---
    print("Training LogisticRegression Classifier...")
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)

    # --- 3. Predictions ---
    y_pred = model.predict(X_test)

    # --- 4. Calculate Metrics ---
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print("\n--- Model Evaluation ---")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("\nConfusion Matrix:")
    print(conf_matrix)

    # --- 5. Save Graphs ---
    
    # Graph 1: Confusion Matrix
    plt.figure(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=["Not Eligible", "Eligible"])
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    cm_path = "results/eligibility_model/confusion_matrix.png"
    plt.savefig(cm_path)
    print(f"\nSaved Confusion Matrix graph to: {cm_path}")
    plt.close() # Close plot to free memory

    # Graph 2: Metrics Bar Chart
    metrics_dict = {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    }
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(metrics_dict.keys(), metrics_dict.values(), color=['#4CAF50', '#2196F3', '#FF9800', '#F44336'])
    plt.ylim(0, 1.1) # Scale from 0 to 1.1 to show text above bars
    plt.title("Model Performance Metrics")
    plt.ylabel("Score")
    
    # Add text labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height, f'{height:.2f}', ha='center', va='bottom')

    metrics_path = "results/eligibility_model/model_metrics.png"
    plt.savefig(metrics_path)
    print(f"Saved Metrics graph to: {metrics_path}")
    plt.close()

    # --- 6. Save Model ---
    # Create src directory if it doesn't exist (just in case)
    if not os.path.exists("src"):
        os.makedirs("src")
        
    output_path = os.path.join("src", "eligibility_model.pkl")
    joblib.dump(model, output_path)
    print(f"\nModel saved to: {output_path}")

if __name__ == "__main__":
    train()