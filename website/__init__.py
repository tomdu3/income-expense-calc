from flask import Flask
from os import environ
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY", "")
    print(environ.get("SECRET_KEY", "no key"))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")
    return app
