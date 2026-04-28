
from flask import Blueprint, request, render_template, redirect, session
from models import db, User, URLHistory
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
auth = Blueprint("auth", __name__)

# ------------------ SIGNUP ------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        # ✅ Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists"

        # ✅ Generate API key (use only ONE method)
        api_key = str(uuid.uuid4())

        user = User(
            username=username,
            password=password,
            api_key=api_key
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")

# ------------------ LOGIN ------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/dashboard")

        return "Invalid login"

    return render_template("login.html")


# ------------------ DASHBOARD ------------------
@auth.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    user = User.query.get(user_id)

    if not user:
        return "User not found"

    # ✅ Fetch URL history
    history = URLHistory.query.filter_by(user_id=user.id).order_by(URLHistory.id.desc()).all()

    return render_template(
        "dashboard.html",
        username=user.username,
        api_key=user.api_key,
        used=user.requests_made,
        remaining=100 - user.requests_made,
        history=history
    )


# ------------------ LOGOUT ------------------
@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")
@auth.route("/clear-history")
def clear_history():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    URLHistory.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return redirect("/dashboard")