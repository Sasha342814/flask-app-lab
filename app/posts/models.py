from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app import db

CATEGORIES = ("news", "publication", "tech", "other")


def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(150), nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(sa.DateTime, default=_utcnow)
    category: Mapped[Optional[str]] = mapped_column(
        sa.Enum(*CATEGORIES, name="post_category"), default="other"
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    author: Mapped[str] = mapped_column(sa.String(20), default="Anonymous")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title!r})>"
