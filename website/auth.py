from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email").strip()
            password = request.form.get("password").strip()
            user = User.query.filter_by(email=email).first()
            if user is not None and check_password_hash(user.password, password):
                flash("Logged in successfully.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Invalid email or password.", category="danger")

                return render_template("login.html", email=email, password=password)
        except Exception as e:
            print(e)
            flash("Invalid email or password.", category="danger")
    else:
        # check is the user is logged in
        if current_user.is_authenticated:
            flash("You are already logged in.", category="danger")
            return redirect(url_for("views.home"))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").strip()
        first_name = request.form.get("firstName").strip()
        last_name = request.form.get("lastName").strip()
        password = request.form.get("password").strip()
        confirm_password = request.form.get("confirmPassword").strip()
        if len(email) < 4:
            flash(
                "Email is too short. Must be at least 4 characters.", category="danger"
            )
        elif len(first_name) < 2 or len(last_name) < 2:
            flash(
                "First name and last name must be at least 2 characters.",
                category="danger",
            )
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", category="danger")
        elif password != confirm_password:
            flash("Passwords do not match.", category="danger")
        else:
            # add user to database
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password, method="pbkdf2:sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)
            flash("User created successfully.", category="success")
            redirect(url_for("views.home"))

        return render_template("register.html", email=email, password=password)

    return render_template("register.html")
