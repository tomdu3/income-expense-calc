from flask import Flask
from os import environ
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.update(
        SECRET_KEY=environ["SECRET_KEY"],  # Will raise KeyError if missing
        SQLALCHEMY_DATABASE_URI=(
            f"postgresql://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@"
            f"{environ['DB_HOST']}:{environ['DB_PORT']}/{environ['POSTGRES_DB']}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_pre_ping": True,  # Helps with connection recycling
            "pool_recycle": 300,  # Recycle connections after 5 minutes
        },
    )

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix="/auth")

    # Database setup
    with app.app_context():
        db.create_all()
        from .models import Category

        Category.insert_default_categories()

    # Login manager setup
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User  # Import here to avoid circular imports

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app
