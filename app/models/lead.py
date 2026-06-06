from app.extensions import db

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=db.func.now())