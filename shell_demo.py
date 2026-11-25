"""Пункт 2: створення користувача з хешованим паролем (аналог flask shell).

python shell_demo.py
"""
from app import bcrypt, create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User(username="yulia12", email="yulia12@gmail.com", password="secret")
    print("пароль у відкритому вигляді:", user.password)

    user.password = bcrypt.generate_password_hash("secret").decode("utf-8")
    print("пароль після хешування:     ", user.password)

    if not db.session.scalar(db.select(User).where(User.email == user.email)):
        db.session.add(user)
        db.session.commit()

    users = db.session.scalars(db.select(User)).all()
    print("користувачі:", users)
    print("check 'secret':", bcrypt.check_password_hash(users[-1].password, "secret"))
    print("check 'wrong': ", bcrypt.check_password_hash(users[-1].password, "wrong"))
