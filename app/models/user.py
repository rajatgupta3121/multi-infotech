from app.extensions import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="student")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))