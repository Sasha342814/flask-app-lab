from sqlalchemy import Boolean, Float, Integer, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    # Зв'язок з продуктами (один до багатьох)
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="select",
    )


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    # server_default потрібен, щоб існуючі рядки отримали значення (NOT NULL)
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=true()
    )

    category_id: Mapped[int | None] = mapped_column(db.ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    def __repr__(self) -> str:
        return f"<Product {self.name} - ${self.price}>"
