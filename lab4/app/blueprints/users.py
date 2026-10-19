from functools import wraps

from flask import (
    Blueprint, flash, make_response, redirect, render_template,
    request, session, url_for,
)

users_bp = Blueprint("users", __name__)

# Заглушка замість бази даних (за умовою завдання)
VALID_USERNAME = "user1"
VALID_PASSWORD = "12345"

# Cookie, які не можна видаляти (інакше користувач вийде з системи)
PROTECTED_COOKIES = {"session"}


def login_required(view):
    """Пускає на сторінку лише якщо користувач є в сесії."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            flash("Спочатку увійдіть у систему!", "danger")
            return redirect(url_for("users.login"))
        return view(*args, **kwargs)
    return wrapped


# ---------- Завдання 1: login / profile / logout ----------

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Wrong data! Try again!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


@users_bp.route("/profile")
@login_required
def profile():
    return render_template(
        "users/profile.html",
        username=session["username"],
        cookies=request.cookies,
    )


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


# ---------- Завдання 2: робота з cookie ----------

@users_bp.route("/cookies/add", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", "").strip()

    if not key:
        flash("Ключ cookie не може бути порожнім.", "danger")
        return redirect(url_for("users.profile"))

    if key in PROTECTED_COOKIES:
        flash(f"Cookie «{key}» службова, її змінювати не можна.", "danger")
        return redirect(url_for("users.profile"))

    if max_age:
        if not max_age.isdigit():
            flash("Термін дії має бути цілим невід'ємним числом (секунди).", "danger")
            return redirect(url_for("users.profile"))
        max_age = int(max_age)
    else:
        max_age = None  # живе до закриття браузера

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, max_age=max_age)
    flash(f"Cookie «{key}» успішно додано.", "success")
    return resp


@users_bp.route("/cookies/delete", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key", "").strip()

    if key in PROTECTED_COOKIES:
        flash(f"Cookie «{key}» службова, її видаляти не можна.", "danger")
        return redirect(url_for("users.profile"))

    if key not in request.cookies:
        flash(f"Cookie з ключем «{key}» не знайдено.", "warning")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.delete_cookie(key)
    flash(f"Cookie «{key}» успішно видалено.", "success")
    return resp


@users_bp.route("/cookies/delete-all", methods=["POST"])
@login_required
def delete_all_cookies():
    resp = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        if key not in PROTECTED_COOKIES:
            resp.delete_cookie(key)
    flash("Усі cookie видалено (крім службової сесії).", "success")
    return resp


# ---------- Завдання 3: кольорова схема ----------

@users_bp.route("/theme/<name>")
@login_required
def set_theme(name):
    if name not in ("light", "dark"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    # Зберігаємо вибір на рік, щоб він діяв і при наступних відвідуваннях
    resp.set_cookie("theme", name, max_age=60 * 60 * 24 * 365)
    flash("Кольорову схему змінено.", "success")
    return resp
