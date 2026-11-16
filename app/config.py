import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Базова конфігурація для всіх середовищ."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Використовується за замовчуванням у режимі розробки."""

    DEBUG = True


class TestingConfig(Config):
    """Конфігурація для тестів: in-memory SQLite, без CSRF."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "testing-secret-key"


class ProductionConfig(Config):
    """Конфігурація для продакшену."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    @classmethod
    def init_app(cls, app):
        if app.config["SECRET_KEY"] == "dev-secret-key-change-me":
            raise RuntimeError("Задайте SECRET_KEY у змінних середовища для production.")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
