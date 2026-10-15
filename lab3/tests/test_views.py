import unittest
from app import app


class MainViewsTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_homepage(self):
        response = self.client.get("/homepage")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Home page".encode(), response.data)

    def test_resume(self):
        self.assertEqual(self.client.get("/resume").status_code, 200)

    def test_contacts(self):
        self.assertEqual(self.client.get("/contacts").status_code, 200)


if __name__ == "__main__":
    unittest.main()
