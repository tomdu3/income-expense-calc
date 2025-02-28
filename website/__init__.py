from flask import Flask
from os import environ, path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY", "")
    app.config["SQLALCHEMY_DATABASE_URI"] =\
        f"sqlite:///{path.join(path.dirname(__file__), DB_NAME)}"  ## overriding default db creation on instance/

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")

    from . import models

    create_database(app)

    return app


def create_database(app):
    with app.app_context():
        if not path.exists(path.join(path.dirname(__file__), DB_NAME)):
            db.create_all()
            print("Created Database!")

