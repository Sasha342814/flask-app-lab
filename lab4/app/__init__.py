from flask import Flask


def create_app():
    app = Flask(__name__)
    # Секретний ключ потрібен для підпису сесії (cookie "session")
    app.config["SECRET_KEY"] = "lab4-dev-secret-change-me"

    from .blueprints.main import main_bp
    from .blueprints.users import users_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix="/users")

    @app.context_processor
    def inject_theme():
        """Робить поточну тему доступною у всіх шаблонах (base.html)."""
        from flask import request
        theme = request.cookies.get("theme", "light")
        return {"theme": theme if theme in ("light", "dark") else "light"}

    return app
