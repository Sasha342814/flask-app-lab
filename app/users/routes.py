from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from app import db
from app.models import User
from app.users.forms import LoginForm, RegistrationForm

user_bp = Blueprint("users", __name__)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    # Авторизованих користувачів перенаправляємо на account
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # 1. витягнути дані з форми, 2. захешувати пароль, 3. зберегти у БД
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=User.hash_password(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", category="success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form, title="Register")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.email == form.email.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You logged in successfully!", "success")
            next_page = request.args.get("next")
            # дозволяємо лише відносні адреси (захист від open redirect)
            if next_page and urlparse(next_page).netloc == "" and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("users.account"))
        flash("Error: Invalid email or password.", "danger")
    return render_template("login.html", form=form, title="Login")


@user_bp.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))


@user_bp.route("/account")
@login_required
def account():
    # current_user - поточний авторизований користувач (об'єкт моделі User)
    return render_template("account.html", user=current_user, title="Account")


@user_bp.route("/users")
@login_required
def users_list():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    return render_template("users.html", users=users, title="Users")
