import unittest
from app import app


class UsersBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        """Тест маршруту /users/hi/<name>."""
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_greetings_without_age(self):
        response = self.client.get("/users/hi/Anna")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ANNA", response.data)

    def test_admin_page(self):
        """Тест маршруту /users/admin, який перенаправляє."""
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_admin_redirect_status(self):
        response = self.client.get("/users/admin")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
