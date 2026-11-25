"""Додавання даних (аналог команд із flask shell у методичці).

python seed.py part1   -> Частина 1: Pc, MAC (модель ще без категорій)
python seed.py part5   -> Частина 5: iPhone 15, категорія Laptops, Gaming Laptop
"""
import sys

from app import create_app, db

app = create_app()


def part1():
    from app.products.models import Product

    p1 = Product(name="Pc", price=700)
    p2 = Product(name="MAC", price=500)
    db.session.add_all([p1, p2])
    db.session.commit()


def part5():
    from app.products.models import Category, Product

    iphone = Product(name="iPhone 15", price=999.99)
    db.session.add(iphone)
    db.session.commit()

    laptops = Category(name="Laptops")
    db.session.add(laptops)
    product = Product(name="Gaming Laptop", price=1500.00, active=False, category=laptops)
    db.session.add(product)
    db.session.commit()

    print(product.category.name)
    print(laptops.products)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    with app.app_context():
        {"part1": part1, "part5": part5}[step]()
    print(f"seed {step}: OK")
