from flask import Blueprint
from flask import render_template

from app.models.course import Course


# =========================================
# BLUEPRINT
# =========================================

main = Blueprint(
    "main",
    __name__
)


# =========================================
# HOME PAGE
# =========================================

@main.route("/")
def home():

    courses = Course.query.all()

    return render_template(
        "home.html",
        courses=courses
    )


# =========================================
# COURSES PAGE
# =========================================

@main.route("/courses")
def courses():

    courses = Course.query.all()

    return render_template(
        "pages/courses.html",
        courses=courses
    )


# =========================================
# CONTACT PAGE
# =========================================

@main.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )