"""Views Tests: коректне завантаження сторінок реєстрації та входу."""


def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Confirm Password" in response.data


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Remember Me" in response.data


def test_home_page_loads(client):
    assert client.get("/").status_code == 200


def test_protected_pages_redirect_anonymous_to_login(client):
    for url in ("/account", "/users"):
        response = client.get(url)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]
