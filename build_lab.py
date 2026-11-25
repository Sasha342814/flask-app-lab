"""Виконує міграції від нуля (4 кроки) і заповнює БД.

python build_lab.py     (venv активовано, з кореня проєкту)
УВАГА: видаляє migrations/ та instance/data.sqlite.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(ROOT, "app", "models.py")
STAGES_DATA = {'models_0_post.py': 'from datetime import datetime\n\nfrom sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text\nfrom sqlalchemy.orm import Mapped, mapped_column, relationship\n\nfrom app import db\n\n\nclass Post(db.Model):\n    __tablename__ = "posts"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    title: Mapped[str] = mapped_column(String(200), nullable=False)\n    content: Mapped[str] = mapped_column(Text, nullable=False)\n    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)\n    publish_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)\n    category: Mapped[str] = mapped_column(String(50), nullable=False)\n    author: Mapped[str] = mapped_column(String(64), nullable=True)\n\n    def __repr__(self) -> str:\n        return f"Post({self.title!r})"\n', 'models_1_user.py': 'from datetime import datetime\n\nfrom sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text\nfrom sqlalchemy.orm import Mapped, mapped_column, relationship\n\nfrom app import db\n\n\nclass User(db.Model):\n    __tablename__ = "users"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)\n    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)\n    password: Mapped[str] = mapped_column(String(255), nullable=False)\n\n    def __repr__(self) -> str:\n        return f"User({self.email!r})"\n\n\nclass Post(db.Model):\n    __tablename__ = "posts"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    title: Mapped[str] = mapped_column(String(200), nullable=False)\n    content: Mapped[str] = mapped_column(Text, nullable=False)\n    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)\n    publish_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)\n    category: Mapped[str] = mapped_column(String(50), nullable=False)\n    author: Mapped[str] = mapped_column(String(64), nullable=True)\n\n    def __repr__(self) -> str:\n        return f"Post({self.title!r})"\n', 'models_2_relation.py': 'from datetime import datetime\n\nfrom sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text\nfrom sqlalchemy.orm import Mapped, mapped_column, relationship\n\nfrom app import db\n\n\nclass User(db.Model):\n    __tablename__ = "users"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)\n    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)\n    password: Mapped[str] = mapped_column(String(255), nullable=False)\n\n    posts: Mapped[list["Post"]] = relationship(\n        back_populates="user", cascade="all, delete-orphan"\n    )\n\n    def __repr__(self) -> str:\n        return f"User({self.email!r})"\n\n\nclass Post(db.Model):\n    __tablename__ = "posts"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    title: Mapped[str] = mapped_column(String(200), nullable=False)\n    content: Mapped[str] = mapped_column(Text, nullable=False)\n    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)\n    publish_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)\n    category: Mapped[str] = mapped_column(String(50), nullable=False)\n\n    # Двосторонній зв\'язок Post <-> User (один користувач -> багато постів)\n    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))\n    user: Mapped["User"] = relationship(back_populates="posts")\n\n    def __repr__(self) -> str:\n        return f"Post({self.title!r})"\n', 'models_3_tags.py': 'from datetime import datetime\n\nfrom sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text\nfrom sqlalchemy.orm import Mapped, mapped_column, relationship\n\nfrom app import db\n\n\n# Асоціативна таблиця для зв\'язку "багато до багатьох"\npost_tags = db.Table(\n    "post_tags",\n    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),\n    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),\n)\n\n\nclass User(db.Model):\n    __tablename__ = "users"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)\n    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)\n    password: Mapped[str] = mapped_column(String(255), nullable=False)\n\n    posts: Mapped[list["Post"]] = relationship(\n        back_populates="user", cascade="all, delete-orphan"\n    )\n\n    def __repr__(self) -> str:\n        return f"User({self.email!r})"\n\n\nclass Post(db.Model):\n    __tablename__ = "posts"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    title: Mapped[str] = mapped_column(String(200), nullable=False)\n    content: Mapped[str] = mapped_column(Text, nullable=False)\n    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)\n    publish_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)\n    category: Mapped[str] = mapped_column(String(50), nullable=False)\n\n    # Двосторонній зв\'язок Post <-> User (один користувач -> багато постів)\n    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))\n    user: Mapped["User"] = relationship(back_populates="posts")\n\n    # Many-to-many з тегами через асоціативну таблицю\n    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")\n\n    def __repr__(self) -> str:\n        return f"Post({self.title!r})"\n\n\nclass Tag(db.Model):\n    __tablename__ = "tags"\n\n    id: Mapped[int] = mapped_column(Integer, primary_key=True)\n    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)\n\n    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")\n\n    def __repr__(self) -> str:\n        return f"Tag({self.name!r})"\n'}
ENV = dict(os.environ, FLASK_APP="run.py", LAB_SKIP_ROUTES="1")


def sh(*args):
    print("\n>", " ".join(args))
    r = subprocess.run([sys.executable, *args], cwd=ROOT, env=ENV)
    if r.returncode != 0:
        sys.exit(f"Помилка ({r.returncode}). Зупинка.")


def flask(*args):
    sh("-m", "flask", *args)


def stage(name):
    print(f"\n=== Модель: {name} ===")
    os.makedirs(os.path.dirname(MODELS), exist_ok=True)
    with open(MODELS, "w", encoding="utf-8") as f:
        f.write(STAGES_DATA[name])


shutil.rmtree(os.path.join(ROOT, "migrations"), ignore_errors=True)
db_file = os.path.join(ROOT, "instance", "data.sqlite")
if os.path.exists(db_file):
    os.remove(db_file)

stage("models_0_post.py")                       # початковий Post (поле author - рядок)
flask("db", "init")
flask("db", "migrate", "-m", "Add Post")
flask("db", "upgrade")

stage("models_1_user.py")                       # п.1-2: User
flask("db", "migrate", "-m", "Add User")
flask("db", "upgrade")

stage("models_2_relation.py")                   # п.3-4: author -> user_id + зв'язок
flask("db", "migrate", "-m", "Replace author with user relationship")
flask("db", "upgrade")

stage("models_3_tags.py")                       # п.9: Tag + post_tags
flask("db", "migrate", "-m", "Add Tag and post_tags many-to-many")
flask("db", "upgrade")

sh("seed.py")
flask("db", "check")
flask("db", "history")
print("\nГОТОВО. Далі: python lab_demo.py ; python measure.py plain ; python measure.py optimized ; python run.py")