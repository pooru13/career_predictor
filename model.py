import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv("career_data.csv")

encoders = {}
for col in df.columns:
    if df[col].dtype == "object":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

X = df.drop("Career", axis=1)
y = df["Career"]

model = DecisionTreeClassifier()
model.fit(X, y)

pickle.dump((model, encoders), open("model.pkl", "wb"))

print("Updated model trained successfully!")
