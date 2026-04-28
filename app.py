from flask import Flask, request, render_template, redirect, session
from models import db, User
from auth import auth
from api import api
from flask_cors import CORS
from models import URLHistory
import pickle
import os
from feature_extraction import extract_features

# ✅ FIRST create app
app = Flask(__name__, template_folder="templates")
CORS(app)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new_database.db"
app.config["SECRET_KEY"] = "secret"

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(api)

# Load model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

if not os.path.exists(model_path):
    raise Exception("model.pkl NOT FOUND")

model = pickle.load(open(model_path, "rb"))

# Create DB tables
with app.app_context():
    db.create_all()


# ✅ NOW define routes (after app is created)

@app.route("/")
def home():
    return "Working on Render 🚀"


@app.route("/test-url", methods=["GET", "POST"])
def test_url():
    if request.method == "POST":

        url = request.form.get("url")
        user_id = session.get("user_id")
        if not user_id:
            return "User ID missing"

        user = User.query.get(user_id)

        if not user:
            return "User not found"

        if user.requests_made >= 100:
            return "Limit reached"

        features = extract_features(url)
        result = model.predict([features])[0]
        status = "Phishing 🚨" if result == 1 else "Legitimate ✅"
        history = URLHistory(
        user_id=user.id,
        url=url,
        result=status
)

        db.session.add(history)
        

        user.requests_made += 1
        db.session.commit()

        return render_template(
            "dashboard.html",
            username=user.username,
            api_key=user.api_key,
            used=user.requests_made,
            remaining=100 - user.requests_made,
            user_id=user.id,
            result="Phishing 🚨" if result == 1 else "Legitimate ✅"
        )

    return "Invalid Request"


@app.route("/api/check-url", methods=["POST"])
def api_check_url():

    api_key = request.headers.get("x-api-key")

    user = User.query.filter_by(api_key=api_key).first()

    if not user:
        return {"error": "Invalid API key"}

    data = request.get_json()

    if not data or "url" not in data:
        return {"error": "URL missing"}

    url = data.get("url")

    features = extract_features(url)
    result = model.predict([features])[0]

    return {
        "url": url,
        "result": "Phishing" if result == 1 else "Legitimate"
    }
    


# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)