import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_name="config.DevConfig"):
    app = Flask(__name__)
    app.config.from_object(config_name)  # налаштування з об'єкта

    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)  # batch потрібен для SQLite
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Налаштування перенаправлення для неавторизованих користувачів
    login_manager.login_view = "users.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    from app import models  # noqa: F401
    from app.main import main_bp
    from app.users.routes import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app
