from app.extensions import db


class Enrollment(db.Model):

    __tablename__ = "enrollment"

    # =========================
    # PRIMARY KEY
    # =========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================
    # FOREIGN KEYS
    # =========================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    # =========================
    # STUDENT DETAILS
    # =========================

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    qualification = db.Column(
        db.String(200)
    )

    batch_time = db.Column(
        db.String(100)
    )

    message = db.Column(
        db.Text
    )

    # =========================
    # COURSE DETAILS
    # =========================

    course_name = db.Column(
        db.String(200)
    )

    course_price = db.Column(
        db.String(50)
    )

    # =========================
    # STATUS
    # =========================

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    payment_status = db.Column(
        db.String(50),
        default="Unpaid"
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )

    # =========================
    # RELATIONSHIPS
    # =========================
# =========================
# RELATIONSHIPS
# =========================

    user = db.relationship(
        "User",
        backref="enrollments"
    )

    course = db.relationship(
        "Course",
        backref="enrollments"
    )
    # =========================
    # STRING REPRESENTATION
    # =========================

    def __repr__(self):

        return f"<Enrollment {self.full_name}>"