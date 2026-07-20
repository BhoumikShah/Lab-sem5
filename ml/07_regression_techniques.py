# 7. Implement Regression Technique and evaluate its performance.

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pandas as pd

# Load Regression Dataset (California Housing)
# (Replace with Kaggle dataset like House Prices using pd.read_csv)
print("Loading dataset...")
data = fetch_california_housing()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split and Scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

def evaluate_regression(name, model):
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)
    
    mse = mean_squared_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds, squared=False)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f"\n--- {name} ---")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R-squared (R2 Score): {r2:.4f}")

# 1. Simple Multiple Linear Regression
evaluate_regression("Linear Regression", LinearRegression())

# 2. Ridge Regression (L2 Regularization)
evaluate_regression("Ridge Regression (alpha=1.0)", Ridge(alpha=1.0))

# 3. Lasso Regression (L1 Regularization)
evaluate_regression("Lasso Regression (alpha=0.1)", Lasso(alpha=0.1))

print("\nEvaluation Notes:")
print("- R2 Score indicates the proportion of variance explained by the model (higher is better, max 1.0).")
print("- RMSE/MAE measure the average error magnitude (lower is better).")
