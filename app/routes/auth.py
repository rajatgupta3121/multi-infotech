from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from app.models.user import User
from app.extensions import db

from app.utils.security import hash_password
from app.utils.security import verify_password


# =========================================
# BLUEPRINT
# =========================================

auth = Blueprint(
    "auth",
    __name__
)


# =========================================
# HELPER FUNCTION
# =========================================

def redirect_user_by_role(user):

    # ADMIN REDIRECT

    if user.role == "admin":

        return redirect(
            url_for("admin.admin_dashboard")
        )

    # STUDENT REDIRECT

    return redirect(
        url_for("student.dashboard")
    )


# =========================================
# REGISTER
# =========================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    # ==============================
    # IF USER ALREADY LOGGED IN
    # ==============================

    if current_user.is_authenticated:

        flash(
            "You are already logged in!",
            "warning"
        )

        return redirect_user_by_role(
            current_user
        )

    # ==============================
    # HANDLE REGISTER FORM
    # ==============================

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # ==========================
        # VALIDATION
        # ==========================

        if not name or not email or not password:

            flash(
                "Please fill all fields.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        # ==========================
        # CHECK EXISTING USER
        # ==========================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already exists!",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        # ==========================
        # HASH PASSWORD
        # ==========================

        hashed_password = hash_password(
            password
        )

        # ==========================
        # CREATE USER
        # ==========================

        new_user = User(

            name=name,

            email=email,

            password=hashed_password,

            role="student"
        )

        db.session.add(new_user)
        db.session.commit()

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html"
    )


# =========================================
# LOGIN
# =========================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    # ==============================
    # IF ALREADY LOGGED IN
    # ==============================

    if current_user.is_authenticated:

        flash(
            "You are already logged in!",
            "info"
        )

        return redirect_user_by_role(
            current_user
        )

    # ==============================
    # HANDLE LOGIN FORM
    # ==============================

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # ==========================
        # VALIDATION
        # ==========================

        if not email or not password:

            flash(
                "Please enter email and password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        # ==========================
        # FIND USER
        # ==========================

        user = User.query.filter_by(
            email=email
        ).first()

        # ==========================
        # VERIFY PASSWORD
        # ==========================

        if user and verify_password(
            password,
            user.password
        ):

            # LOGIN USER

            login_user(user)

            flash(
                f"Welcome {user.name}!",
                "success"
            )

            return redirect_user_by_role(
                user
            )

        else:

            flash(
                "Invalid email or password!",
                "danger"
            )

    return render_template(
        "auth/login.html"
    )


# =========================================
# LOGOUT
# =========================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully!",
        "success"
    )

    return redirect(
        url_for("main.home")
    )