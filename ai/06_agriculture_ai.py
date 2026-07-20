from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

df = pd.read_csv('crop_recommendation.csv')

X = df.drop('label', axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print(f"Model Accuracy on Test Data: {accuracy_score(y_test, preds):.4f}\n")

if __name__ == '__main__':
    print("Enter soil/weather parameters to predict the best crop:")
    try:
        n = float(input("Nitrogen (N) content: "))
        p = float(input("Phosphorus (P) content: "))
        k = float(input("Potassium (K) content: "))
        temp = float(input("Temperature (C): "))
        hum = float(input("Humidity (%): "))
        ph = float(input("Soil pH: "))
        rain = float(input("Rainfall (mm): "))
        
        new_data = pd.DataFrame([[n, p, k, temp, hum, ph, rain]], columns=X.columns)
        prediction = model.predict(new_data)
        
        print(f"\n--> Recommended Crop to Plant: {prediction[0].upper()}")
    except ValueError:
        print("Invalid input. Please enter numerical values.")
