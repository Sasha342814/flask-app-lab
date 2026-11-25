"""Тестування входу і виходу користувача."""
from tests.conftest import login, register


def test_login_success_redirects_to_account(client):
    register(client)
    response = login(client)
    assert response.status_code == 302
    assert "/account" in response.headers["Location"]


def test_account_page_after_login(client):
    register(client)
    login(client)
    response = client.get("/account")
    assert response.status_code == 200
    assert b"Welcome, testuser!" in response.data
    assert b"test@example.com" in response.data


def test_navbar_changes_after_login(client):
    register(client)
    before = client.get("/").data
    assert b"Login" in before and b"Register" in before
    assert b"Logout" not in before

    login(client)
    after = client.get("/").data
    assert b"Account" in after and b"Logout" in after
    assert b"Register" not in after


def test_login_wrong_password(client):
    register(client)
    response = login(client, password="wrong-password", follow=True)
    assert b"Invalid email or password" in response.data
    # доступ до захищеної сторінки не відкрито
    assert client.get("/account").status_code == 302


def test_login_unknown_user(client):
    response = login(client, email="nobody@example.com", follow=True)
    assert b"Invalid email or password" in response.data


def test_logout(client):
    register(client)
    login(client)
    assert client.get("/account").status_code == 200

    response = client.get("/logout", follow_redirects=True)
    assert b"You have successfully logged out." in response.data
    # після виходу сторінка знову захищена
    assert client.get("/account").status_code == 302


def test_authenticated_user_redirected_from_register_and_login(client):
    register(client)
    login(client)
    for url in ("/register", "/login"):
        response = client.get(url)
        assert response.status_code == 302
        assert "/account" in response.headers["Location"]


def test_users_list_requires_login_and_shows_count(client):
    register(client)
    login(client)
    response = client.get("/users")
    assert response.status_code == 200
    assert b"Users List (1)" in response.data
