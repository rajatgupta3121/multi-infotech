from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from app.extensions import db

from app.models.course import Course
from app.models.enrollment import Enrollment


courses = Blueprint(
    "courses",
    __name__
)


# =========================================
# SHOW ALL COURSES
# =========================================

@courses.route("/courses")
def course_list():

    all_courses = Course.query.order_by(
        Course.id.desc()
    ).all()

    return render_template(
        "pages/courses.html",
        courses=all_courses
    )


# =========================================
# ENROLLMENT PAGE
# =========================================

@courses.route(
    "/enroll/<int:course_id>",
    methods=["GET", "POST"]
)
@login_required
def enroll(course_id):

    # GET COURSE

    course = Course.query.get_or_404(
        course_id
    )

    # CHECK ALREADY ENROLLED

    existing_enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course.id
    ).first()

    if existing_enrollment:

        flash(
            "You are already enrolled in this course.",
            "warning"
        )

        return redirect(
            url_for("courses.course_list")
        )

    # HANDLE FORM SUBMISSION

    if request.method == "POST":

        phone = request.form.get(
            "phone"
        )

        qualification = request.form.get(
            "qualification"
        )

        # CREATE ENROLLMENT

        new_enrollment = Enrollment(

            user_id=current_user.id,

            course_id=course.id,

            full_name=current_user.name,

            email=current_user.email,

            phone=phone,

            qualification=qualification,

            course_name=course.title,

            course_price=course.fees,

            status="Pending",

            payment_status="Unpaid"
        )

        db.session.add(
            new_enrollment
        )

        db.session.commit()

        flash(
            "Enrollment successful!",
            "success"
        )

        return redirect(
            url_for(
                "courses.admission_success"
            )
        )

    return render_template(
        "pages/enroll.html",
        course=course
    )


# =========================================
# ADMISSION SUCCESS PAGE
# =========================================

@courses.route("/admission-success")
@login_required
def admission_success():

    return render_template(
        "pages/admission_success.html"
    )