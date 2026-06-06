from flask import Flask
from config import Config
from app.extensions import db, login_manager, mail
from app.routes.courses import courses
from app.routes.student import student
from app.routes.admin import admin
from app.routes.contact import contact
from app.routes.chatbot import chatbot
from app.routes.dashboard import dashboard

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # register routes
    from app.routes.main import main
    from app.routes.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(courses)
    app.register_blueprint(student)
    app.register_blueprint(admin)
    app.register_blueprint(contact)
    mail.init_app(app)
    app.register_blueprint(chatbot)
    app.register_blueprint(dashboard)
   

    return app