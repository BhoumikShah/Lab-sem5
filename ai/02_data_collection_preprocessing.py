import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import urllib.request
import json

print(" Data Collection ")
data_dict = {
    'Age': [25, 30, np.nan, 45, 50],
    'Salary': [50000, 60000, 80000, np.nan, 120000],
    'City': ['New York', 'Paris', 'London', 'Paris', 'New York']
}
df = pd.DataFrame(data_dict)
print("Initial Dataset:\n", df)

print("\nFetching data from dummy API (JSON)...")
try:
    with urllib.request.urlopen("https://jsonplaceholder.typicode.com/users/1") as url:
        api_data = json.loads(url.read().decode())
        print(f"API Fetched User: {api_data['name']} from {api_data['address']['city']}")
except Exception as e:
    print("API fetch failed (possibly offline).")

print("\n--- Data Preprocessing ---")
print("1. Imputing Missing Values (Mean strategy):")
imputer = SimpleImputer(strategy='mean')
df[['Age', 'Salary']] = imputer.fit_transform(df[['Age', 'Salary']])
print(df[['Age', 'Salary']])

print("\n2. One-Hot Encoding (City column):")
encoder = OneHotEncoder(sparse_output=False)
city_encoded = encoder.fit_transform(df[['City']])
city_encoded_df = pd.DataFrame(city_encoded, columns=encoder.get_feature_names_out(['City']))
df_preprocessed = pd.concat([df, city_encoded_df], axis=1).drop('City', axis=1)
print(df_preprocessed)

print("\n3. Feature Scaling (Age and Salary):")
scaler = StandardScaler()
df_preprocessed[['Age', 'Salary']] = scaler.fit_transform(df_preprocessed[['Age', 'Salary']])
print(df_preprocessed)
