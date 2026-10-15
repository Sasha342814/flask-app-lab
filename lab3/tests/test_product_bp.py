import unittest
from app import app
from app.products.views import products


class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list(self):
        """Список товарів відображає всі товари."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        for product in products:
            self.assertIn(product["name"].encode(), response.data)

    def test_product_detail(self):
        """Детальна сторінка товару за id."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_detail_each(self):
        for product in products:
            response = self.client.get(f"/products/{product['id']}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(product["name"].encode(), response.data)

    def test_product_not_found(self):
        """Неіснуючий id повертає 404."""
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

    def test_product_invalid_id_type(self):
        """Нечисловий id не відповідає маршруту -> 404."""
        response = self.client.get("/products/abc")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
