"""Insert data into products table

Revision ID: 21c4b3574567
Revises: 75fee4b7247d
Create Date: 2026-11-25 21:35:05.449255

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '21c4b3574567'
down_revision = '75fee4b7247d'
branch_labels = None
depends_on = None


def upgrade():
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
