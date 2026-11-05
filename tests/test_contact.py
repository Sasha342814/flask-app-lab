import os
import unittest

from app import app, LOG_DIR


class ContactFormTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  # у тестах вимикаємо CSRF
        self.client = app.test_client()
        self.log_path = os.path.join(LOG_DIR, 'contact.log')

    def valid_data(self, **kw):
        data = {"name": "Іван", "email": "ivan@example.com", "phone": "",
                "topic": "question", "message": "Це тестове повідомлення."}
        data.update(kw)
        return data

    def test_get_form(self):
        r = self.client.get("/contact")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"<form", r.data)

    def test_valid_post_redirects_and_logs(self):
        r = self.client.post("/contact", data=self.valid_data(name="Тестер"))
        self.assertEqual(r.status_code, 302)  # PRG
        r = self.client.post("/contact", data=self.valid_data(name="Тестер"), follow_redirects=True)
        self.assertIn("Дякуємо".encode(), r.data)
        with open(self.log_path, encoding="utf-8") as f:
            self.assertIn("Тестер", f.read())

    def test_invalid_email(self):
        r = self.client.post("/contact", data=self.valid_data(email="bad"))
        self.assertEqual(r.status_code, 200)
        self.assertIn("Некоректна адреса".encode(), r.data)

    def test_short_message(self):
        r = self.client.post("/contact", data=self.valid_data(message="hi"))
        self.assertIn("від 10 до 1000".encode(), r.data)

    def test_topic_required(self):
        r = self.client.post("/contact", data=self.valid_data(topic=""))
        self.assertIn("Оберіть тему".encode(), r.data)


if __name__ == "__main__":
    unittest.main()
