import io
import os
import shutil
import tempfile
import unittest

import base64
from tinydb import TinyDB

from app import app
from app.products import db


# найменший валідний PNG 1x1 (без залежності від Pillow)
PNG_BYTES = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==')


def make_image(fmt='PNG', name='pic.png'):
    return io.BytesIO(PNG_BYTES), name


class ProductsCRUDTestCase(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False,
                          PRODUCTS_DB_PATH=os.path.join(self.tmp, 'products.json'),
                          UPLOAD_FOLDER=os.path.join(self.tmp, 'uploads'))
        db.init_db(app)  # створює файл і 3 початкові товари
        self.client = app.test_client()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def data(self, **kw):
        d = {'name': 'Monitor', 'content': 'Гарний монітор 27 дюймів', 'price': '199.99',
             'category': 'electronics', 'quantity': '3'}
        d.update(kw)
        return d

    def post(self, url, **kw):
        return self.client.post(url, data=self.data(**kw), content_type='multipart/form-data')

    # ---- Read
    def test_list(self):
        r = self.client.get('/product/')
        self.assertEqual(r.status_code, 200)
        for n in (b'Laptop', b'Phone', b'PC'):
            self.assertIn(n, r.data)

    def test_detail(self):
        r = self.client.get('/product/2')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Phone', r.data)

    def test_detail_not_found(self):
        self.assertEqual(self.client.get('/product/999').status_code, 404)

    # ---- Create
    def test_add_product_prg_and_db(self):
        r = self.post('/product/add')
        self.assertEqual(r.status_code, 302)
        with app.app_context():
            p = db.get_by_id(4)
        self.assertEqual(p['name'], 'Monitor')
        self.assertEqual(p['price'], 199.99)
        self.assertTrue(p['created_at'])
        self.assertIsNone(p['image'])
        r = self.client.get('/product/')
        self.assertIn(b'Monitor', r.data)

    def test_add_flash_success(self):
        r = self.client.post('/product/add', data=self.data(), follow_redirects=True,
                             content_type='multipart/form-data')
        self.assertIn('Товар успішно додано'.encode(), r.data)

    def test_add_validation_errors(self):
        for bad, text in [({'name': 'ab'}, 'щонайменше 3'),
                          ({'price': '-5'}, 'додатною'),
                          ({'price': '1.999'}, 'двох знаків'),
                          ({'quantity': '-1'}, 'від’ємною'),
                          ({'quantity': ''}, 'Вкажіть ціле число'),
                          ({'price': 'abc'}, 'Вкажіть ціну'),
                          ({'category': 'nope'}, 'Оберіть категорію зі списку')]:
            r = self.post('/product/add', **bad)
            self.assertEqual(r.status_code, 200, bad)
            self.assertIn(text.encode(), r.data, bad)
        with app.app_context():
            self.assertEqual(len(db.get_all()), 3)

    def test_add_with_image(self):
        buf, name = make_image()
        d = self.data(); d['image'] = (buf, name)
        r = self.client.post('/product/add', data=d, content_type='multipart/form-data')
        self.assertEqual(r.status_code, 302)
        with app.app_context():
            p = db.get_by_id(4)
        self.assertTrue(p['image'].startswith('uploads/'))
        self.assertNotEqual(os.path.basename(p['image']), name)  # UUID-ім'я
        self.assertTrue(os.path.isfile(os.path.join(self.tmp, p['image'])))

    def test_reject_wrong_extension(self):
        d = self.data(); d['image'] = (io.BytesIO(b'hello'), 'virus.exe')
        r = self.client.post('/product/add', data=d, content_type='multipart/form-data')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Дозволені лише'.encode(), r.data)

    def test_file_too_large(self):
        old = app.config['MAX_CONTENT_LENGTH']
        app.config['MAX_CONTENT_LENGTH'] = 1000
        try:
            d = self.data(); d['image'] = (io.BytesIO(b'x' * 5000), 'big.png')
            r = self.client.post('/product/add', data=d, content_type='multipart/form-data')
            self.assertEqual(r.status_code, 302)
        finally:
            app.config['MAX_CONTENT_LENGTH'] = old

    # ---- Update
    def test_edit_get_prefilled(self):
        r = self.client.get('/product/1/edit')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Laptop', r.data)

    def test_edit_keeps_id_and_created_at(self):
        with app.app_context():
            before = db.get_by_id(1)
        r = self.post('/product/1/edit', name='Laptop Pro', price='1500')
        self.assertEqual(r.status_code, 302)
        with app.app_context():
            after = db.get_by_id(1)
        self.assertEqual(after['name'], 'Laptop Pro')
        self.assertEqual(after['price'], 1500.0)
        self.assertEqual(after['id'], 1)
        self.assertEqual(after['created_at'], before['created_at'])

    def test_edit_replace_image(self):
        buf, name = make_image()
        d = self.data(); d['image'] = (buf, name)
        self.client.post('/product/1/edit', data=d, content_type='multipart/form-data')
        with app.app_context():
            first = db.get_by_id(1)['image']
        buf, name = make_image('JPEG', 'new.jpg')
        d = self.data(); d['image'] = (buf, name)
        self.client.post('/product/1/edit', data=d, content_type='multipart/form-data')
        with app.app_context():
            second = db.get_by_id(1)['image']
        self.assertNotEqual(first, second)
        self.assertFalse(os.path.isfile(os.path.join(self.tmp, first)))  # старе видалено
        # без нового файлу — зображення зберігається
        self.post('/product/1/edit')
        with app.app_context():
            self.assertEqual(db.get_by_id(1)['image'], second)

    def test_edit_invalid(self):
        r = self.post('/product/1/edit', name='x')
        self.assertEqual(r.status_code, 200)
        with app.app_context():
            self.assertEqual(db.get_by_id(1)['name'], 'Laptop')

    def test_edit_not_found(self):
        self.assertEqual(self.client.get('/product/999/edit').status_code, 404)

    # ---- Delete
    def test_delete_only_post(self):
        self.assertEqual(self.client.get('/product/1/delete').status_code, 405)

    def test_delete(self):
        r = self.client.post('/product/1/delete', follow_redirects=True)
        self.assertIn('видалено'.encode(), r.data)
        self.assertEqual(self.client.get('/product/1').status_code, 404)

    def test_delete_not_found(self):
        self.assertEqual(self.client.post('/product/999/delete').status_code, 404)

    # ---- Storage
    def test_data_persists_and_id_unique(self):
        self.post('/product/add')
        self.client.post('/product/4/delete')
        self.post('/product/add', name='Another')
        with app.app_context():
            ids = [p['id'] for p in db.get_all()]
        self.assertEqual(len(ids), len(set(ids)))
        with TinyDB(app.config['PRODUCTS_DB_PATH']) as t:  # файл існує й читається
            self.assertEqual(len(t.table('products')), 4)

    def test_seed_images_shown(self):
        r = self.client.get('/product/1')
        self.assertIn(b'images/seed/laptop.jpg', r.data)

    def test_missing_image_placeholder(self):
        self.post('/product/add')  # новий товар без фото
        r = self.client.get('/product/4')
        self.assertIn(b'no-image.svg', r.data)

    def test_csrf_enforced(self):
        app.config['WTF_CSRF_ENABLED'] = True
        r = self.client.post('/product/add', data=self.data(), content_type='multipart/form-data')
        self.assertEqual(r.status_code, 400)  # CSRFProtect відхиляє запит без токена
        with app.app_context():
            self.assertEqual(len(db.get_all()), 3)


if __name__ == '__main__':
    unittest.main()
