from flask import request, redirect, url_for, render_template, flash

from . import app


@app.route("/")
def main():
    return render_template("index.html", title="Головна")


@app.route("/homepage")
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("homepage.html", title="Homepage", agent=agent)


# ---- Маршрути з lab2 ----
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        # Форма-заглушка: реальної відправки немає
        name = request.form.get("name", "").strip()
        flash(f"Дякуємо, {name or 'друже'}! Повідомлення отримано (заглушка).", "success")
        return redirect(url_for("contacts"))
    return render_template("contacts.html", title="Контакти")
