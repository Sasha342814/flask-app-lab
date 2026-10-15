from flask import Blueprint

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
    template_folder="templates",
)

from . import views  # noqa: E402,F401
