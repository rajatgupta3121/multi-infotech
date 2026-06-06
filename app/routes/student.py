from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from app.models.enrollment import Enrollment
from app.models.course import Course


student = Blueprint(
    "student",
    __name__
)


# =========================================
# STUDENT DASHBOARD
# =========================================

@student.route("/dashboard")
@login_required
def dashboard():

    # =====================================
    # BLOCK ADMIN ACCESS
    # =====================================

    if current_user.role == "admin":

        flash(
            "Admins cannot access student dashboard.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_dashboard")
        )

    # =====================================
    # GET STUDENT ENROLLMENTS
    # =====================================

    enrollments = Enrollment.query.filter_by(
        user_id=current_user.id
    ).all()

    # =====================================
    # FETCH COURSES
    # =====================================

    courses = []

    for enrollment in enrollments:

        course = Course.query.get(
            enrollment.course_id
        )

        if course:

            courses.append(course)

    # =====================================
    # RENDER DASHBOARD
    # =====================================

    return render_template(
        "student/dashboard.html",
        courses=courses
    )