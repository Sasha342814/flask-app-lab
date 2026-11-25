import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    # Частина 3: єдиний стиль іменування обмежень
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    db.init_app(app)
    # render_as_batch=True обов'язковий для SQLite (він не вміє ALTER для обмежень)
    migrate.init_app(app, db, render_as_batch=True)

    from app.products import models  # noqa: F401  (щоб Alembic бачив моделі)

    return app
