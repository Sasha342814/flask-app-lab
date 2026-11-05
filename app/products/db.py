"""Робота з TinyDB: JSON-файл data/products.json, таблиця 'products'."""
import os
from datetime import datetime

from flask import current_app
from tinydb import TinyDB, Query

SEED = [
    {"name": "Laptop", "price": 1200.0, "category": "electronics", "quantity": 10, "image": "images/seed/laptop.jpg",
     "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам’яті та SSD на 512 ГБ."},
    {"name": "Phone", "price": 800.0, "category": "electronics", "quantity": 25, "image": "images/seed/phone.jpg",
     "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год."},
    {"name": "PC", "price": 1800.0, "category": "electronics", "quantity": 5, "image": "images/seed/pc.jpg",
     "content": "Настільний комп’ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD."},
]


def _open():
    path = current_app.config['PRODUCTS_DB_PATH']
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return TinyDB(path, ensure_ascii=False, indent=2, encoding='utf-8')


def now_iso():
    return datetime.now().isoformat(timespec='seconds')


def init_db(app):
    """Створює сховище й таблицю; якщо вона порожня — додає початкові товари."""
    with app.app_context():
        with _open() as db:
            table = db.table('products')
            if len(table) == 0:
                for i, item in enumerate(SEED, start=1):
                    table.insert({**item, "id": i, "created_at": now_iso()})


def get_all():
    with _open() as db:
        return sorted(db.table('products').all(), key=lambda p: p['id'])


def get_by_id(product_id):
    with _open() as db:
        return db.table('products').get(Query().id == product_id)


def add(data):
    """Додає товар, автоматично задаючи id та created_at. Повертає id."""
    with _open() as db:
        table = db.table('products')
        new_id = max((p['id'] for p in table.all()), default=0) + 1
        table.insert({**data, "id": new_id, "created_at": now_iso()})
        return new_id


def update(product_id, data):
    """Оновлює поля товару; id та created_at не змінюються."""
    data = {k: v for k, v in data.items() if k not in ('id', 'created_at')}
    with _open() as db:
        updated = db.table('products').update(data, Query().id == product_id)
        return bool(updated)


def delete(product_id):
    with _open() as db:
        return bool(db.table('products').remove(Query().id == product_id))
