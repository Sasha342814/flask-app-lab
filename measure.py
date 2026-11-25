"""Пункт 13: порівняння запитів без options() та з joinedload/selectinload.

Кожен варіант запускайте ОКРЕМО (нова ORM-сесія):
    python measure.py plain
    python measure.py optimized
"""
import os
import sys

os.environ["SQL_ECHO"] = "1"  # журнал SQL у консоль

from sqlalchemy import event, select
from sqlalchemy.orm import joinedload, selectinload

from app import create_app, db
from app.models import Post

mode = sys.argv[1] if len(sys.argv) > 1 else "plain"
app = create_app()

counter = {"select": 0}

with app.app_context():
    @event.listens_for(db.engine, "before_cursor_execute")
    def count_selects(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            counter["select"] += 1

    if mode == "plain":
        stmt = select(Post).order_by(Post.id.desc())
    else:
        stmt = (
            select(Post)
            .options(joinedload(Post.user), selectinload(Post.tags))
            .order_by(Post.id.desc())
        )

    posts = db.session.scalars(stmt).all()
    for post in posts:
        print(post.title, post.user.username, [tag.name for tag in post.tags])

    print("\n" + "=" * 50)
    print(f"Варіант: {mode}")
    print(f"Кількість дописів: {len(posts)}")
    print(f"Кількість SELECT:  {counter['select']}")
    print("=" * 50)
