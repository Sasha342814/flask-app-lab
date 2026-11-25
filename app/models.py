from flask_login import UserMixin

from app import bcrypt, db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    # id із сесії приходить рядком - перетворюємо на int
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # bcrypt-хеш = 60 символів

    def __repr__(self) -> str:
        return f"User({self.username!r}, {self.email!r})"

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
