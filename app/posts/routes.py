from flask import Blueprint, abort, redirect, render_template, url_for
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app import db
from app.models import Post, Tag, User
from app.posts.forms import PostForm

post_bp = Blueprint("posts", __name__)


@post_bp.route("/")
def index():
    stmt = (
        select(Post)
        .options(joinedload(Post.user), selectinload(Post.tags))
        .order_by(Post.id.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("index.html", posts=posts)


@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    stmt = (
        select(Post)
        .options(joinedload(Post.user), selectinload(Post.tags))
        .where(Post.id == post_id)
    )
    post = db.session.scalars(stmt).first()
    if post is None:
        abort(404)
    return render_template("post_detail.html", post=post)


@post_bp.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    # Пункт 8: автори з БД (синтаксис SQLAlchemy 2.0)
    authors = db.session.scalars(select(User).order_by(User.id)).all()
    form.author_id.choices = [(a.id, a.username) for a in authors]

    # Пункт 11: теги з БД
    all_tags = db.session.scalars(select(Tag).order_by(Tag.id)).all()
    form.tags.choices = [(t.id, t.name) for t in all_tags]

    if form.validate_on_submit():
        selected = []
        if form.tags.data:
            selected = db.session.scalars(
                select(Tag).where(Tag.id.in_(form.tags.data))
            ).all()
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            publish_date=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data,
            tags=selected,
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("posts.post_detail", post_id=post.id))

    return render_template("add_post.html", form=form)
