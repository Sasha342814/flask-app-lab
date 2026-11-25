# Лабораторна «Зв'язки. Міграції» (Flask + SQLAlchemy + Flask-Migrate)

## Запуск (Windows, PowerShell / CMD)

```
cd lab7
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python build_lab.py
python show_db.py
```

(Linux/macOS: `source .venv/bin/activate` замість `.venv\Scripts\activate`.)

`build_lab.py` з нуля виконує всі частини роботи: створює `migrations/`, робить 5 міграцій
(Add Product, Add category, Add active column, Add created_at, Insert data), додає дані
з Частини 1 і 5 та в кінці виводить `flask db check`, `current`, `heads`, `history`.

## Скріни для звіту (тільки остаточні)

1. **Схема таблиць** — DB Browser for SQLite: відкрити `instance/data.sqlite`,
   вкладка *Database Structure* (розгорнути `products`, `categories`, `alembic_version`).
   Або: `python show_db.py` — верхня частина виводу.
2. **Дані в БД** — DB Browser, вкладка *Browse Data*: окремо `products`, `categories`.
   Або нижня частина виводу `python show_db.py`.
3. **Історія міграцій** — у терміналі (з активованим venv):
   ```
   flask db history
   ```
   Має бути 5 ревізій, остання з `(head)`.

## Ручні команди (якщо потрібно показати кожен крок окремо)

```
flask db current
flask db heads
flask db check
flask db history
flask db downgrade     # відкат на одну міграцію
flask db upgrade       # знову вперед
```

Папка `stages/` містить версії моделі `Product/Category` для кожного кроку.
Файл `app/products/models.py` — остаточна версія.

Щоб почати заново: просто повторно запустіть `python build_lab.py`
(видаляє `migrations/` та `instance/data.sqlite`).
