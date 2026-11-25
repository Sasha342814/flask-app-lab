"""Тестові дані: 2 автори, 3 теги, 5 постів (пункти 5-6, 10, 13)."""
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import Post, Tag, User

app = create_app()

with app.app_context():
    u1 = User(username="user1", email="user1@ex.com", password=generate_password_hash("1111"))
    u2 = User(username="user2", email="user2@ex.com", password=generate_password_hash("2222"))
    tech, art, science = Tag(name="Tech"), Tag(name="Art"), Tag(name="Science")
    db.session.add_all([u1, u2, tech, art, science])
    db.session.commit()

    now = datetime.now()
    posts = [
        Post(title="Art of pop culture", content="test content test content", category="art",
             publish_date=now - timedelta(days=4), user_id=u1.id),
        Post(title="Python tips", content="test content test content", category="tech",
             publish_date=now - timedelta(days=3), user_id=u1.id),
        Post(title="Space news", content="test content test content", category="tech",
             publish_date=now - timedelta(days=2), user_id=u2.id),
        Post(title="Digital painting", content="test content test content", category="art",
             publish_date=now - timedelta(days=1), user_id=u2.id),
        Post(title="AI and science", content="test content test content", category="tech",
             publish_date=now, user_id=u1.id),
    ]
    db.session.add_all(posts)
    db.session.commit()

    # many-to-many: один пост має кілька тегів, один тег належить кільком постам
    posts[0].tags.append(art)
    posts[0].tags.append(tech)
    posts[0].tags.append(science)
    posts[1].tags.append(tech)
    posts[2].tags.append(science)
    posts[2].tags.append(tech)
    posts[3].tags.append(art)
    posts[4].tags.append(tech)
    posts[4].tags.append(science)
    db.session.commit()
    print("Seed OK: users=2, tags=3, posts=5")
