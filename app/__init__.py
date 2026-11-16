import os

from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from app.config import config


class Base(DeclarativeBase):
    """Базовий клас моделей (стиль SQLAlchemy 2.0)."""


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name=None):
    """Application factory: створює застосунок залежно від назви конфігурації."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")
    cfg = config.get(config_name, config["default"])

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(cfg)
    if hasattr(cfg, "init_app"):
        cfg.init_app(app)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Імпорт моделей, щоб Flask-Migrate їх бачив
    from app.posts import post_bp
    from app.posts import models  # noqa: F401

    app.register_blueprint(post_bp)

    @app.route("/")
    def home():
        return redirect(url_for("posts.all_posts"))

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
