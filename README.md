# Лабораторна 6: ORM, SQLAlchemy, CRUD (Flask)

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
```

## Частина 2: Flask shell (скріншоти для звіту)

```
flask shell
>>> from app import db
>>> from app.posts.models import Post
>>> db.create_all()
>>> db.session.add_all([Post(title="Django", content="Framework"), Post(title="Flask", content="Micro"), Post(title="ORM", content="SQLAlchemy")])
>>> db.session.commit()
>>> posts = db.session.scalars(db.select(Post).order_by(Post.title.asc())).all()
>>> posts
>>> post = db.get_or_404(Post, 3)
>>> db.session.delete(post); db.session.commit()
>>> db.session.scalars(db.select(Post)).all()
>>> db.drop_all()
```
Після цього видаліть папку `instance/` вручну.

## Частина 3: міграції

```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
Потім (поля is_active, author вже є в моделі — щоб показати другу міграцію,
спершу закоментуйте їх, зробіть першу міграцію, потім розкоментуйте):
```
flask db migrate -m "add is_active, author"
flask db upgrade
```

## Запуск застосунку і тестів

```
flask run
python -m unittest discover -s tests -v
```
