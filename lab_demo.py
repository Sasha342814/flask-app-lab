"""Пункти 7 і 10 (те, що в методичці робиться через flask shell).

python lab_demo.py
"""
from sqlalchemy import select

from app import create_app, db
from app.models import Post, Tag, User

app = create_app()

with app.app_context():
    # п.7 - пости користувачів id=2 та id=1
    u2 = db.session.get(User, 2)
    u1 = db.session.get(User, 1)
    print("Пости user id=2:", u2.posts)
    print("Пости user id=1:", u1.posts)

    # п.10 - теги поста та пости тегу
    post = db.session.get(Post, 1)
    print("Теги поста 1:", post.tags)
    tag = db.session.scalars(select(Tag).where(Tag.name == "Tech")).one()
    print("Пости тегу Tech:", tag.posts)

    # приклад append() для нового тегу
    new_tag = db.session.scalars(select(Tag).where(Tag.name == "News")).first() or Tag(name="News")
    if new_tag not in post.tags:
        post.tags.append(new_tag)
        db.session.commit()
    print("Теги поста 1 після append:", post.tags)
