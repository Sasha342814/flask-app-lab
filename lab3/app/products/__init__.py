from flask import Blueprint

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
    template_folder="templates",
)

from . import views  # noqa: E402,F401
