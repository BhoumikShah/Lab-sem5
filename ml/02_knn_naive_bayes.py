# 2. Implement KNN and Naïve Bayes classifiers for the given data. Compare the metric values.

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Load Data (Replace with pd.read_csv for Kaggle datasets)
data = load_breast_cancer()
X = data.data
y = data.target

# Split and Scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 1. K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
y_pred_knn = knn.predict(X_test_scaled)

# 2. Naive Bayes (Gaussian)
nb = GaussianNB()
nb.fit(X_train_scaled, y_train)
y_pred_nb = nb.predict(X_test_scaled)

# Evaluation Function
def evaluate_model(name, y_true, y_pred):
    print(f"\n--- {name} Performance ---")
    print(f"Accuracy : {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall   : {recall_score(y_true, y_pred):.4f}")
    print(f"F1-Score : {f1_score(y_true, y_pred):.4f}")

evaluate_model("KNN", y_test, y_pred_knn)
evaluate_model("Naïve Bayes", y_test, y_pred_nb)

print("\nComparison:")
print("KNN is sensitive to feature scaling, hence data was standardized.")
print("Naïve Bayes assumes feature independence, which may not hold true, but it often performs surprisingly well.")
