import pytest

from app import create_app, db


@pytest.fixture
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, username="testuser", email="test@example.com",
             password="secret123", confirm=None, follow=False):
    return client.post("/register", data={
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": confirm if confirm is not None else password,
    }, follow_redirects=follow)


def login(client, email="test@example.com", password="secret123", follow=False):
    return client.post("/login", data={"email": email, "password": password},
                       follow_redirects=follow)
