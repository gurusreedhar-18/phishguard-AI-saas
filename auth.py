from flask import Blueprint, request, render_template, redirect, url_for
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from utils import generate_api_key

auth = Blueprint("auth", __name__)


# 🔐 Signup Route
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Try another."

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        user = User(
            username=username,
            password=hashed_password,
            api_key=generate_api_key()
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# 🔐 Login Route
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        # Validate user
        if user and check_password_hash(user.password, password):
            return redirect(url_for("auth.dashboard", user_id=user.id))

        return "Invalid username or password"

    return render_template("login.html")


# 📊 Dashboard Route
@auth.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    user = User.query.get(user_id)

    if not user:
        return "User not found"

    return render_template(
        "dashboard.html",
        username=user.username,
        api_key=user.api_key,
        used=user.requests_made,
        remaining=100 - user.requests_made,
        user_id=user.id   # ✅ VERY IMPORTANT (fixes your issue)
    )