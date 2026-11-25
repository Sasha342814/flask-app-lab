"""Тестування збереження користувача у БД при реєстрації."""
from sqlalchemy import select

from app import bcrypt, db
from app.models import User
from tests.conftest import register


def test_successful_registration_saves_user(client, app):
    response = register(client)
    assert response.status_code == 302            # redirect на /login
    assert "/login" in response.headers["Location"]

    user = db.session.scalar(select(User).where(User.email == "test@example.com"))
    assert user is not None
    assert user.username == "testuser"


def test_password_is_hashed(client, app):
    register(client, password="secret123")
    user = db.session.scalar(select(User).where(User.username == "testuser"))
    assert user.password != "secret123"
    assert user.password.startswith("$2b$")
    assert len(user.password) == 60
    assert bcrypt.check_password_hash(user.password, "secret123")
    assert user.check_password("secret123")
    assert not user.check_password("wrong-password")


def test_duplicate_email_rejected(client, app):
    register(client)
    response = register(client, username="another", email="test@example.com", follow=True)
    assert b"Email is already registered." in response.data
    assert len(db.session.scalars(select(User)).all()) == 1


def test_duplicate_username_rejected(client, app):
    register(client)
    response = register(client, username="testuser", email="other@example.com", follow=True)
    assert b"Username is already taken." in response.data
    assert len(db.session.scalars(select(User)).all()) == 1


def test_invalid_email_rejected(client, app):
    response = register(client, email="not-an-email", follow=True)
    assert response.status_code == 200
    assert db.session.scalars(select(User)).all() == []


def test_password_mismatch_rejected(client, app):
    response = register(client, confirm="different", follow=True)
    assert b"Passwords must match." in response.data
    assert db.session.scalars(select(User)).all() == []
