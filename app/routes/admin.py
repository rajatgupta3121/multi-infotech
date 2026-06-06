from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

from flask_login import login_required

from werkzeug.utils import secure_filename

import os
import uuid

from app.extensions import db

from app.models.user import User
from app.models.lead import Lead
from app.models.chat import ChatMessage
from app.models.course import Course
from app.models.enrollment import Enrollment

from app.utils.decorators import admin_required


admin = Blueprint(
    "admin",
    __name__
)


# =========================================
# ADMIN DASHBOARD
# =========================================

@admin.route("/admin")
@login_required
@admin_required
def admin_dashboard():

    total_students = User.query.filter_by(
        role="student"
    ).count()

    total_leads = Lead.query.count()

    total_courses = Course.query.count()

    total_messages = ChatMessage.query.count()

    total_enrollments = Enrollment.query.count()

    recent_leads = Lead.query.order_by(
        Lead.id.desc()
    ).limit(5).all()

    recent_chats = ChatMessage.query.order_by(
        ChatMessage.id.desc()
    ).limit(10).all()

    recent_enrollments = Enrollment.query.order_by(
        Enrollment.id.desc()
    ).limit(10).all()

    courses = Course.query.order_by(
        Course.id.desc()
    ).all()

    return render_template(
        "admin/dashboard.html",

        total_students=total_students,
        total_leads=total_leads,
        total_courses=total_courses,
        total_messages=total_messages,
        total_enrollments=total_enrollments,

        recent_leads=recent_leads,
        recent_chats=recent_chats,
        recent_enrollments=recent_enrollments,

        courses=courses
    )


# =========================================
# COURSES MANAGEMENT
# =========================================

@admin.route("/admin/courses")
@login_required
@admin_required
def admin_courses():

    courses = Course.query.order_by(
        Course.id.desc()
    ).all()

    return render_template(
        "admin/courses.html",
        courses=courses
    )


# =========================================
# ADD COURSE
# =========================================

@admin.route(
    "/admin/courses/add",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def add_course():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        duration = request.form.get("duration")
        fees = request.form.get("fees")
        category = request.form.get("category")
        level = request.form.get("level")

        image_file = request.files.get("image")

        if not title or not description:

            flash(
                "Please fill all required fields.",
                "danger"
            )

            return redirect(request.url)

        filename = "default-course.jpg"

        if image_file and image_file.filename != "":

            unique_name = str(uuid.uuid4())

            filename = secure_filename(
                unique_name + "_" + image_file.filename
            )

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            image_path = os.path.join(
                upload_folder,
                filename
            )

            image_file.save(image_path)

        course = Course(

            title=title,
            description=description,
            duration=duration,
            fees=fees,
            category=category,
            level=level,
            image=filename
        )

        db.session.add(course)
        db.session.commit()

        flash(
            "Course added successfully!",
            "success"
        )

        return redirect(
            url_for("admin.admin_courses")
        )

    return render_template(
        "admin/add_course.html"
    )


# =========================================
# EDIT COURSE
# =========================================

@admin.route(
    "/admin/course/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_course(id):

    course = Course.query.get_or_404(id)

    if request.method == "POST":

        course.title = request.form.get("title")
        course.description = request.form.get("description")
        course.duration = request.form.get("duration")
        course.fees = request.form.get("fees")
        course.category = request.form.get("category")
        course.level = request.form.get("level")

        image_file = request.files.get("image")

        if image_file and image_file.filename != "":

            if course.image and course.image != "default-course.jpg":

                old_path = os.path.join(
                    current_app.root_path,
                    "static",
                    "uploads",
                    course.image
                )

                if os.path.exists(old_path):

                    os.remove(old_path)

            unique_name = str(uuid.uuid4())

            filename = secure_filename(
                unique_name + "_" + image_file.filename
            )

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            upload_path = os.path.join(
                upload_folder,
                filename
            )

            image_file.save(upload_path)

            course.image = filename

        db.session.commit()

        flash(
            "Course updated successfully!",
            "success"
        )

        return redirect(
            url_for("admin.admin_courses")
        )

    return render_template(
        "admin/edit_course.html",
        course=course
    )


# =========================================
# DELETE COURSE
# =========================================

@admin.route("/admin/course/delete/<int:id>")
@login_required
@admin_required
def delete_course(id):

    course = Course.query.get_or_404(id)

    if course.image and course.image != "default-course.jpg":

        image_path = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            course.image
        )

        if os.path.exists(image_path):

            os.remove(image_path)

    enrollments = Enrollment.query.filter_by(
        course_id=course.id
    ).all()

    for enrollment in enrollments:

        db.session.delete(enrollment)

    db.session.delete(course)

    db.session.commit()

    flash(
        "Course deleted successfully.",
        "warning"
    )

    return redirect(
        url_for("admin.admin_courses")
    )


# =========================================
# ENROLLMENTS MANAGEMENT
# =========================================

@admin.route("/admin/enrollments")
@login_required
@admin_required
def admin_enrollments():

    enrollments = Enrollment.query.order_by(
        Enrollment.id.desc()
    ).all()

    return render_template(
        "admin/enrollments.html",
        enrollments=enrollments
    )


# =========================================
# DELETE ENROLLMENT
# =========================================

@admin.route("/admin/enrollment/delete/<int:id>")
@login_required
@admin_required
def delete_enrollment(id):

    enrollment = Enrollment.query.get_or_404(id)

    db.session.delete(enrollment)

    db.session.commit()

    flash(
        "Enrollment deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.admin_enrollments")
    )


# =========================================
# AI CHAT MANAGEMENT
# =========================================

@admin.route("/admin/ai-chats")
@login_required
@admin_required
def admin_ai_chats():

    chats = ChatMessage.query.order_by(
        ChatMessage.id.desc()
    ).all()

    return render_template(
        "admin/ai_chats.html",
        chats=chats
    )


# =========================================
# ANALYTICS
# =========================================

@admin.route("/admin/analytics")
@login_required
@admin_required
def analytics():

    total_students = User.query.filter_by(
        role="student"
    ).count()

    total_courses = Course.query.count()

    total_enrollments = Enrollment.query.count()

    total_messages = ChatMessage.query.count()

    return render_template(
        "admin/analytics.html",

        total_students=total_students,
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_messages=total_messages
    )