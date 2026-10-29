import unittest
from app import app


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def login(self, user="admin", pwd="12345"):
        return self.client.post("/users/login", data={"username": user, "password": pwd},
                                follow_redirects=True)

    def test_profile_requires_login(self):
        r = self.client.get("/users/profile", follow_redirects=True)
        self.assertIn("Спочатку увійдіть".encode(), r.data)

    def test_login_success(self):
        r = self.login()
        self.assertIn("Вітаємо, admin".encode(), r.data)

    def test_login_fail(self):
        r = self.login(pwd="wrong")
        self.assertIn("Невірний логін".encode(), r.data)

    def test_logout(self):
        self.login()
        r = self.client.post("/users/logout", follow_redirects=True)
        self.assertIn("Ви вийшли".encode(), r.data)
        r = self.client.get("/users/profile", follow_redirects=True)
        self.assertIn("Спочатку увійдіть".encode(), r.data)

    def test_add_and_delete_cookie(self):
        self.login()
        r = self.client.post("/users/cookies/add", data={"key": "foo", "value": "bar", "max_age": "60"},
                             follow_redirects=True)
        self.assertIn(b"foo", r.data)
        r = self.client.post("/users/cookies/delete", data={"key": "foo"}, follow_redirects=True)
        self.assertIn("видалено".encode(), r.data)

    def test_theme_persisted(self):
        self.login()
        r = self.client.get("/users/theme/dark", follow_redirects=True)
        self.assertIn(b"theme-dark", r.data)


if __name__ == "__main__":
    unittest.main()
