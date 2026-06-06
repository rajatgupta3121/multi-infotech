from app.extensions import db


class Course(db.Model):

    __tablename__ = "course"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    duration = db.Column(
        db.String(100)
    )

    fees = db.Column(
        db.String(100)
    )

    category = db.Column(
        db.String(100)
    )

    level = db.Column(
        db.String(100)
    )

    image = db.Column(
        db.String(300)
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    def __repr__(self):

        return f"<Course {self.title}>"