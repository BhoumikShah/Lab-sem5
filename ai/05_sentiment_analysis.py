import os
import re
import pandas as pd
import kagglehub
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("Loading dataset from Kaggle...")
dataset_dir = kagglehub.dataset_download("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews")
df = pd.read_csv(os.path.join(dataset_dir, "IMDB Dataset.csv"))

def clean(text):
    return re.sub(r'<[^>]*>', ' ', text).lower()

df['review'] = df['review'].apply(clean)

print("Training sentiment classifier...")
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train = vectorizer.fit_transform(df_train['review'])
X_test = vectorizer.transform(df_test['review'])

y_train = df_train['sentiment'].map({'positive': 1, 'negative': 0})
y_test = df_test['sentiment'].map({'positive': 1, 'negative': 0})

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, preds):.4f}\n")

# 5. Predict sentiment for 10 random test reviews
print("=" * 60)
print("             PREDICTIONS ON 10 RANDOM REVIEWS              ")
print("=" * 60)

sample_df = df_test.sample(10, random_state=42)
for idx, row in sample_df.iterrows():
    raw_review = row['review']
    actual = row['sentiment'].capitalize()
    
    vec = vectorizer.transform([raw_review])
    pred_label = model.predict(vec)[0]
    pred = "Positive" if pred_label == 1 else "Negative"
    
    display_text = raw_review[:120] + "..." if len(raw_review) > 120 else raw_review
    print(f"Review: '{display_text}'")
    print(f"-> Actual: {actual} | Predicted: {pred}\n")
