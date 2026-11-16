from flask import Blueprint

post_bp = Blueprint(
    "posts",
    __name__,
    template_folder="templates/posts",
    static_folder="static",
    static_url_path="/posts/static",
    url_prefix="/post",
)

from . import views  # noqa: E402,F401  # Імпортує маршрути
