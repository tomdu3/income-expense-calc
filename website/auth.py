from flask import Blueprint, render_template, request, flash

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
            flash("User created successfully.", category="success")

        return render_template("register.html", email=email, password=password)

    return render_template("register.html")
