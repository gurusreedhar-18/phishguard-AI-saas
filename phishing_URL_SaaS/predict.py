import joblib
from feature_extraction import extract_features

# Load trained AI model
model = joblib.load("model.pkl")

# Test URLs (you can change or add more)
test_urls = [
    "http://google.com",
    "http://free-paypal-login.xyz",
    "http://amazon.in",
    "http://secure-bank-update.info"
]

# Predict each URL
for url in test_urls:
    features = extract_features(url)
    prediction = model.predict([features])[0]
    
    if prediction == 1:
        print(f" {url} → Phishing URL")
    else:
        print(f" {url} → Legitimate URL")