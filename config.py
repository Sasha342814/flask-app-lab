import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "dev-secret-key"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "data.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Пункт 13: журналювання SQL. Вмикається змінною середовища SQL_ECHO=1
SQLALCHEMY_ECHO = os.environ.get("SQL_ECHO") == "1"
