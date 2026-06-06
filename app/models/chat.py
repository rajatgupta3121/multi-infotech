from app.extensions import db

class ChatMessage(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.String(200))

    role = db.Column(db.String(50))
    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=db.func.now())