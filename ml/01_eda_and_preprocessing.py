import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler

if os.path.exists("Breast_Cancer.csv"):
    df = pd.read_csv("Breast_Cancer.csv")
else:
    import kagglehub
    df = pd.read_csv(os.path.join(kagglehub.dataset_download("reihanenamdari/breast-cancer"), "Breast_Cancer.csv"))

print(df.shape)
print(df.head())
print(df.describe())
print(df.isnull().sum())

sns.countplot(x='Status', data=df, hue='Status', legend=False, palette='Set2')
plt.title("Status Distribution")
plt.show()

cols = ['Age', 'Tumor Size', 'Regional Node Examined', 'Reginol Node Positive', 'Survival Months']
sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

scaler = StandardScaler()
minmax = MinMaxScaler()
scale_cols = ['Age', 'Tumor Size']
print(scaler.fit_transform(df[scale_cols])[:5])
print(minmax.fit_transform(df[scale_cols])[:5])

categorical_cols = ['Race', 'Marital Status', 'Status']
for col in categorical_cols:
    encoder = LabelEncoder()
    df[f'encoded_{col}'] = encoder.fit_transform(df[col])
    print(df[[col, f'encoded_{col}']].drop_duplicates().head())
