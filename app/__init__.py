import logging
import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-in-production'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['PRODUCTS_DB_PATH'] = os.path.join(BASE_DIR, 'data', 'products.json')
app.config['UPLOAD_FOLDER'] = None  # None -> app/products/static/uploads
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 МБ

# Захист від CSRF для всіх форм
csrf = CSRFProtect(app)

# Логер для контактної форми: дописує у файл logs/contact.log
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
contact_logger = logging.getLogger('contact')
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    _handler = logging.FileHandler(os.path.join(LOG_DIR, 'contact.log'), encoding='utf-8')
    _handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
    contact_logger.addHandler(_handler)

# Імпорти після створення app, щоб уникнути циклічних залежностей
from . import views  # noqa: E402,F401
from .users.views import users_bp  # noqa: E402
from .products.views import products_bp  # noqa: E402

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)

from .products.db import init_db  # noqa: E402
init_db(app)
