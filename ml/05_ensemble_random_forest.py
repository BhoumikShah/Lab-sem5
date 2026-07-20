# 5. Implementation of Ensemble, Random Forests. Analyze the performance.

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load Data
data = load_breast_cancer()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Random Forest (Ensemble of Decision Trees)
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train, y_train)
rf_preds = rf_clf.predict(X_test)

# Analyze Performance
accuracy = accuracy_score(y_test, rf_preds)
print(f"--- Random Forest Classifier ---")
print(f"Accuracy: {accuracy:.4f}")

# Feature Importance Analysis
feature_importances = pd.Series(rf_clf.feature_importances_, index=data.feature_names)
top_features = feature_importances.nlargest(10)

print("\nTop 5 Most Important Features:")
print(top_features.head())

# Plot Feature Importances
plt.figure(figsize=(10, 6))
top_features.plot(kind='barh', color='teal')
plt.title("Top 10 Feature Importances in Random Forest")
plt.gca().invert_yaxis()
plt.show()

# Plot Confusion Matrix
cm = confusion_matrix(y_test, rf_preds)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Random Forest Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
