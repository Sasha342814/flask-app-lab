import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # --- допоміжні функції ---
    def _add_post(self, title="Test", content="Some content", **kwargs):
        with self.app.app_context():
            post = Post(title=title, content=content, **kwargs)
            db.session.add(post)
            db.session.commit()
            return post.id

    def _form_data(self, **overrides):
        data = {
            "title": "My first post",
            "content": "This is TDD!",
            "is_active": "y",
            "publish_date": "2025-01-01T10:00",
            "category": "tech",
        }
        data.update(overrides)
        return data

    # --- US01: створення ---
    def test_create_post_form_displayed(self):
        response = self.client.get("/post/create")
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(
            "/post/create", data=self._form_data(), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post added successfully", response.data)

        with self.app.app_context():
            post = db.session.scalar(db.select(Post).filter_by(title="My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")
            self.assertEqual(post.category, "tech")
            self.assertEqual(post.author, "Anonymous")
            self.assertEqual(post.posted, datetime(2025, 1, 1, 10, 0))

    def test_create_post_author_from_session(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "alex"
        self.client.post("/post/create", data=self._form_data())
        with self.app.app_context():
            post = db.session.scalar(db.select(Post))
            self.assertEqual(post.author, "alex")

    def test_create_post_validation_error(self):
        response = self.client.post(
            "/post/create", data=self._form_data(title="a"), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter the correct data in the form!", response.data)
        with self.app.app_context():
            self.assertEqual(len(db.session.scalars(db.select(Post)).all()), 0)

    # --- US02: список ---
    def test_list_posts(self):
        self._add_post(title="Older", posted=datetime(2024, 1, 1))
        self._add_post(title="Newer", posted=datetime(2025, 1, 1))
        self._add_post(title="Hidden", is_active=False)

        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode()
        self.assertIn("Older", html)
        self.assertIn("Newer", html)
        self.assertNotIn("Hidden", html)
        # спадання за датою: Newer раніше за Older
        self.assertLess(html.index("Newer"), html.index("Older"))

    # --- US03: деталі ---
    def test_view_post_detail(self):
        post_id = self._add_post(title="Detail title", content="Detail body")
        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail title", response.data)
        self.assertIn(b"Detail body", response.data)

    # --- US04: редагування ---
    def test_update_post_form_prefilled(self):
        post_id = self._add_post(title="Old title")
        response = self.client.get(f"/post/{post_id}/update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Old title", response.data)

    def test_update_post(self):
        post_id = self._add_post(title="Old title", content="Old content")
        response = self.client.post(
            f"/post/{post_id}/update",
            data=self._form_data(title="New title", content="New content"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post updated successfully", response.data)
        with self.app.app_context():
            post = db.session.get(Post, post_id)
            self.assertEqual(post.title, "New title")
            self.assertEqual(post.content, "New content")

    # --- US05: видалення ---
    def test_delete_confirm_page(self):
        post_id = self._add_post(title="To delete")
        response = self.client.get(f"/post/{post_id}/delete")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"To delete", response.data)
        with self.app.app_context():
            self.assertIsNotNone(db.session.get(Post, post_id))

    def test_delete_post(self):
        post_id = self._add_post(title="To delete")
        response = self.client.post(
            f"/post/{post_id}/delete", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post deleted successfully", response.data)
        with self.app.app_context():
            self.assertIsNone(db.session.get(Post, post_id))

    # --- US06: 404 ---
    def test_404_not_found(self):
        response = self.client.get("/post/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page Not Found", response.data)

    def test_404_unknown_url(self):
        response = self.client.get("/no-such-page")
        self.assertEqual(response.status_code, 404)

    def test_update_delete_404(self):
        self.assertEqual(self.client.get("/post/9999/update").status_code, 404)
        self.assertEqual(self.client.post("/post/9999/delete").status_code, 404)


if __name__ == "__main__":
    unittest.main()
