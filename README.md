# Лабораторна робота №5 — Flask-WTF, TinyDB (завдання 1 і 2)

```
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
flask run                                  # http://127.0.0.1:8080  (або python run.py)
python -m unittest discover tests -v       # тести
```

Маршрути: `/`, `/resume`, `/contacts`, `/users/hi/<name>?age=30`, `/users/admin` (редірект),
`/products/`, `/products/<id>`.

Git: `git checkout lab2 && git checkout -b lab3`, комміти після кожного завдання, скріни — для звіту.

## Лаба 4
Вхід: `/users/login` (логін `admin`, пароль `12345` — заглушка у `app/users/views.py`).
Профіль `/users/profile`: привітання, вихід, керування кукі (додати/видалити/видалити всі), таблиця кукі,
вибір світлої/темної схеми (зберігається у кукі `theme`). Flash-повідомлення з категоріями — у `base.html`.
Git: `git checkout lab3 && git checkout -b lab4`.

## Лаба 5, завдання 1
Форма: `/contact`, клас `ContactForm` у `app/forms.py`, макрос `render_field` у `app/templates/macros.html`,
дані пишуться у `logs/contact.log`. CSRF увімкнено глобально (`CSRFProtect`).
Потрібно `pip install -r requirements.txt` (додано Flask-WTF та email-validator).
Git: `git checkout lab4 && git checkout -b lab5`, коміт, напр. `feat: add Flask-WTF contact form`.
