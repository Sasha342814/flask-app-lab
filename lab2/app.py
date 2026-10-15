from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "lab2-secret-key"  # потрібен для flash-повідомлень


@app.route("/")
def resume():
    # title передається в шаблон динамічно
    return render_template("resume.html", title="Резюме")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        # Форма-заглушка: реальної відправки немає
        name = request.form.get("name", "").strip()
        flash(f"Дякуємо, {name or 'друже'}! Повідомлення отримано (заглушка).", "success")
        return redirect(url_for("contacts"))
    return render_template("contacts.html", title="Контакти")


if __name__ == "__main__":
    app.run(debug=True)
