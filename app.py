from flask import Flask, request, render_template
from models import db, User
from auth import auth
from api import api
import pickle
import os
from feature_extraction import extract_features

# ✅ FIRST create app
app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///database.db")
app.config["SECRET_KEY"] = "secret"

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(api)

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Create DB tables
with app.app_context():
    db.create_all()


# ✅ NOW define routes (after app is created)

@app.route("/")
def home():
    return "<h2>Welcome to PhishGuard AI 🚀</h2><p>Go to /signup</p>"


@app.route("/test-url", methods=["GET", "POST"])
def test_url():
    if request.method == "POST":

        url = request.form.get("url")
        user_id = request.form.get("user_id")
        if not user_id:
         return "User ID missing"

        user = User.query.get(user_id)

        if not user:
            return "User not found"

        if user.requests_made >= 100:
            return "Limit reached"

        features = extract_features(url)
        result = model.predict([features])[0]

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


# Run app
if __name__ == "__main__":
    app.run(debug=True)

