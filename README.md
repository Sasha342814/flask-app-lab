# Лабораторна робота №4 — request, сесії та кукі

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
