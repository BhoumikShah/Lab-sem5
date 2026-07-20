from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

data = load_breast_cancer()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

preds = model.predict(X_test_scaled)
print(f"Diagnosis Accuracy: {accuracy_score(y_test, preds):.4f}\n")

target_names = ['Malignant (Cancerous)', 'Benign (Safe)']
print("Classification Report:")
print(classification_report(y_test, preds, target_names=target_names))

if __name__ == '__main__':
    print("\n--- Patient Diagnosis Simulation ---")
    sample_patient = X_test_scaled[0].reshape(1, -1)
    
    prob = model.predict_proba(sample_patient)[0]
    prediction = model.predict(sample_patient)[0]
    
    print(f"Probability of Malignant: {prob[0]*100:.2f}%")
    print(f"Probability of Benign: {prob[1]*100:.2f}%")
    
    diagnosis = target_names[prediction]
    print(f"\n--> AI Diagnosis: {diagnosis}")
