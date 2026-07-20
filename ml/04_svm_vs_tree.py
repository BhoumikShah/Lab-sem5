# 4. Implementation of SVM. Comparison with Tree-Based Classifier.

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Data
X, y = load_breast_cancer(return_X_y=True)

# Split and Scale
# SVM requires feature scaling to perform optimally
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train SVM
svm_clf = SVC(kernel='rbf', random_state=42)
svm_clf.fit(X_train_scaled, y_train)
svm_preds = svm_clf.predict(X_test_scaled)

# Train Decision Tree
tree_clf = DecisionTreeClassifier(random_state=42)
tree_clf.fit(X_train_scaled, y_train) # Using scaled data for fair comparison, though trees don't require it
tree_preds = tree_clf.predict(X_test_scaled)

# Compare
print("--- Support Vector Machine (SVM) ---")
print(f"Accuracy: {accuracy_score(y_test, svm_preds):.4f}")
print(classification_report(y_test, svm_preds))

print("\n--- Decision Tree Classifier ---")
print(f"Accuracy: {accuracy_score(y_test, tree_preds):.4f}")
print(classification_report(y_test, tree_preds))

print("\nComparison Analysis:")
print("SVM generally performs better on high-dimensional data and finds a clear margin of separation.")
print("Decision Trees are highly interpretable but are prone to overfitting without pruning.")
