import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from feature_extraction import extract_features

# Load dataset
data = pd.read_csv("dataset.csv")

# Prepare data
X = data["url"].apply(extract_features).tolist()
y = data["label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===== AI PART (MODEL TRAINING) =====
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save trained AI model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" AI model trained successfully and saved as model.pkl")

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)