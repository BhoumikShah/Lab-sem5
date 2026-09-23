import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

API_KEY = "579b464db66ec23bdd000001746b938745aa48755cc791137850987f"
RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070" 

url = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=json&limit=2000"

try:
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    
    df = pd.DataFrame(json_data['records'])
    df = df.dropna()
    
    le_state = LabelEncoder()
    le_season = LabelEncoder()
    
    df['state_encoded'] = le_state.fit_transform(df['state_name'])
    df['season_encoded'] = le_season.fit_transform(df['season'])
    
    df['area'] = pd.to_numeric(df['area'], errors='coerce')
    df['production'] = pd.to_numeric(df['production'], errors='coerce')
    df = df.dropna()
    
    X = df[['state_encoded', 'season_encoded', 'area', 'production']]
    y = df['crop']
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    
    sample_state = df['state_encoded'].iloc[0]
    sample_season = df['season_encoded'].iloc[0]
    sample_data = pd.DataFrame([[sample_state, sample_season, 5000, 10000]], columns=X.columns)
    
    print("Data loaded directly from data.gov.in!")
    print("Predicted/Expected Crop:", model.predict(sample_data)[0])

except Exception as e:
    print("Error fetching or processing data:", e)