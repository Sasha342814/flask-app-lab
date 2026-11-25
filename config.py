import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class DevConfig:
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False      # щоб тести могли надсилати форми без CSRF-токена
    BCRYPT_LOG_ROUNDS = 4         # швидше хешування у тестах
