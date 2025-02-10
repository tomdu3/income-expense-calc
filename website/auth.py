from flask import Blueprint, render_template, request

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text="Testing", username="tom", boolean=False)


@auth.route("/logout")
def logout():
    return "<p>logout</p>"  # TODO - this will be replaced with a logout function


@auth.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
