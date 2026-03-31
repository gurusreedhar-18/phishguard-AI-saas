from flask import Blueprint, request, jsonify
from models import User, db
import pickle
from feature_extraction import extract_features

api = Blueprint("api", __name__)
model = pickle.load(open("model.pkl", "rb"))

@api.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()

    api_key = data.get("api_key")
    url = data.get("url")

    user = User.query.filter_by(api_key=api_key).first()

    if not user:
        return jsonify({"error": "Invalid API Key"})

    if user.requests_made >= 100:
        return jsonify({"error": "Limit reached"})

    features = extract_features(url)
    result = model.predict([features])[0]

    user.requests_made += 1
    db.session.commit()

    return jsonify({
        "result": "Phishing" if result == 1 else "Legitimate",
        "remaining": 100 - user.requests_made
    })