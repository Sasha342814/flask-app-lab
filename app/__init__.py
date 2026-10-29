from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-in-production'

# Імпорти після створення app, щоб уникнути циклічних залежностей
from . import views  # noqa: E402,F401
from .users.views import users_bp  # noqa: E402
from .products.views import products_bp  # noqa: E402

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
