from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.course import Course
from app.models.enrollment import Enrollment

dashboard = Blueprint(
    "dashboard",
    __name__
)


@dashboard.route("/dashboard")
@login_required
def student_dashboard():

    # Admin Redirect
    if current_user.role == "admin":

        return render_template(
            "admin/dashboard_redirect.html"
        )

    # Get Student Enrollments
    enrollments = Enrollment.query.filter_by(
        user_id=current_user.id
    ).all()

    # Get Enrolled Courses
    courses = []

    for enrollment in enrollments:

        course = Course.query.get(
            enrollment.course_id
        )

        if course:
            courses.append(course)

    # Dashboard Analytics
    total_courses = len(courses)

    # Temporary Progress Logic
    if total_courses > 0:

        overall_progress = min(
            total_courses * 20,
            100
        )

    else:

        overall_progress = 0

    # Temporary Certificates Logic
    certificates_earned = (
        total_courses // 3
    )

    completed_courses = certificates_earned

    # Learning Level
    if overall_progress >= 80:

        learning_level = "Pro"

    elif overall_progress >= 50:

        learning_level = "Intermediate"

    else:

        learning_level = "Beginner"

    # Recent Courses
    recent_courses = courses[:3]

    return render_template(
        "student/dashboard.html",

        student=current_user,

        courses=courses,

        recent_courses=recent_courses,

        enrollments=enrollments,

        total_courses=total_courses,

        completed_courses=completed_courses,

        certificates_earned=certificates_earned,

        overall_progress=overall_progress,

        learning_level=learning_level
    )