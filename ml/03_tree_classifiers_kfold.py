# 3. Implementation of Tree-based Classifiers. Apply K-Fold Cross Validation.

from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold, cross_val_score
import matplotlib.pyplot as plt
from sklearn import tree

# Load Data (Replace with your Kaggle CSV)
X, y = load_breast_cancer(return_X_y=True)

# Initialize Decision Tree Classifier
dt_classifier = DecisionTreeClassifier(random_state=42, max_depth=4)

# Apply K-Fold Cross Validation
k = 5
kfold = KFold(n_splits=k, shuffle=True, random_state=42)

# Calculate Cross-Validation Scores
cv_results = cross_val_score(dt_classifier, X, y, cv=kfold, scoring='accuracy')

print(f"--- K-Fold Cross Validation (K={k}) ---")
print(f"Accuracies for each fold: {cv_results}")
print(f"Mean Accuracy: {cv_results.mean():.4f}")
print(f"Standard Deviation: {cv_results.std():.4f}")

# Train on full dataset to visualize
dt_classifier.fit(X, y)

# Plotting the tree (simplified)
plt.figure(figsize=(15, 10))
tree.plot_tree(dt_classifier, filled=True, rounded=True, max_depth=3)
plt.title("Decision Tree Visualization (Max Depth = 3)")
plt.show()
