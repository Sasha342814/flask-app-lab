"""Автоматично виконує всю лабораторну: усі міграції від нуля.

Запуск (з активованим venv, з кореня проєкту):
    python build_lab.py

УВАГА: видаляє папку migrations та базу instance/data.sqlite і створює їх заново.
"""
import glob
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(ROOT, "app", "products", "models.py")
STAGES = os.path.join(ROOT, "stages")

ENV = dict(os.environ, FLASK_APP="run.py")


def sh(*args):
    print("\n>", " ".join(args))
    r = subprocess.run([sys.executable, *args], cwd=ROOT, env=ENV)
    if r.returncode != 0:
        sys.exit(f"Команда завершилась з помилкою ({r.returncode}). Зупинка.")


def flask(*args):
    sh("-m", "flask", *args)


def use_stage(name):
    print(f"\n=== Модель: {name} ===")
    shutil.copy(os.path.join(STAGES, name), MODELS)


DATA_MIGRATION = '''def upgrade():
    conn = op.get_bind()

    categories_table = table(
        "categories", column("id", sa.Integer), column("name", sa.String)
    )
    products_table = table(
        "products",
        column("name", sa.String),
        column("price", sa.Float),
        column("active", sa.Boolean),
        column("category_id", sa.Integer),
    )

    # --- Вставка категорій ---
    op.bulk_insert(categories_table, [
        {"name": "Electronics"},
        {"name": "Books"},
        {"name": "Clothing"},
    ])

    # id категорії шукаємо за назвою (id=1 вже зайнятий категорією Laptops)
    def cid(name):
        return conn.execute(
            sa.text("SELECT id FROM categories WHERE name = :n"), {"n": name}
        ).scalar()

    # --- Вставка продуктів ---
    op.bulk_insert(products_table, [
        {"name": "Laptop", "price": 1200.0, "active": True, "category_id": cid("Electronics")},
        {"name": "Smartphone", "price": 800.0, "active": True, "category_id": cid("Electronics")},
        {"name": "Novel", "price": 20.0, "active": True, "category_id": cid("Books")},
        {"name": "T-Shirt", "price": 25.0, "active": False, "category_id": cid("Clothing")},
    ])


def downgrade():
    # Видаляємо тільки вставлені продукти та категорії
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt');
    """)
    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)
'''


def write_data_migration():
    files = glob.glob(os.path.join(ROOT, "migrations", "versions", "*insert_data_into_products_table.py"))
    if not files:
        sys.exit("Не знайдено файл міграції з даними")
    path = files[0]
    with open(path, encoding="utf-8") as f:
        src = f.read()
    head = src.split("def upgrade():")[0]
    if "from sqlalchemy.sql import table, column" not in head:
        head = head.replace(
            "import sqlalchemy as sa\n",
            "import sqlalchemy as sa\nfrom sqlalchemy.sql import table, column\n",
            1,
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + DATA_MIGRATION)
    print("Файл міграції з даними заповнено:", os.path.basename(path))


def main():
    # 0. чистий старт
    shutil.rmtree(os.path.join(ROOT, "migrations"), ignore_errors=True)
    db_file = os.path.join(ROOT, "instance", "data.sqlite")
    if os.path.exists(db_file):
        os.remove(db_file)

    # Частина 1
    use_stage("models_1_product.py")
    flask("db", "init")
    flask("db", "migrate", "-m", "Add Product")
    flask("db", "upgrade")
    sh("seed.py", "part1")

    # Частини 2-3 (naming_convention вже є в app/__init__.py)
    use_stage("models_2_category.py")
    flask("db", "migrate", "-m", "Add category")
    flask("db", "upgrade")

    # Частина 4
    use_stage("models_3_active.py")
    flask("db", "migrate", "-m", "Add active column to products")
    flask("db", "upgrade")

    # Частина 6
    use_stage("models_4_created_at.py")
    flask("db", "migrate", "-m", "Add created_at with server_default")
    flask("db", "upgrade")

    # Частина 5
    sh("seed.py", "part5")

    # Частина 7
    flask("db", "revision", "-m", "Insert data into products table")
    write_data_migration()
    flask("db", "upgrade")

    # Перевірки
    flask("db", "check")
    flask("db", "current")
    flask("db", "heads")
    flask("db", "history")

    print("\nГОТОВО. Тепер: python show_db.py  (схема + дані для скрінів)")


if __name__ == "__main__":
    main()
