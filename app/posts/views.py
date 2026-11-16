from datetime import datetime, timezone

from flask import flash, redirect, render_template, request, session, url_for

from app import db
from app.posts import post_bp
from app.posts.forms import PostForm
from app.posts.models import Post


@post_bp.route("")
def all_posts():
    stmt = (
        db.select(Post).where(Post.is_active.is_(True)).order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/<int:id>")
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)


@post_bp.route("/create", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            category=form.category.data,
            # Автор — користувач із сесії, інакше Anonymous
            author=(session.get("username") or "Anonymous")[:20],
        )
        if form.publish_date.data:
            new_post.posted = form.publish_date.data
        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.all_posts"))  # PRG
    if request.method == "POST":
        flash("Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form, title="Create a New Post")


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if request.method == "GET":
        # Назви publish_date (форма) і posted (модель) не збігаються
        form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        if form.publish_date.data:
            post.posted = form.publish_date.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    if request.method == "POST":
        flash("Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form, title="Edit Post")


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "danger")
        return redirect(url_for("posts.all_posts"))
    return render_template("delete_confirm.html", post=post)
