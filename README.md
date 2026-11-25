# Лабораторна: реєстрація та вхід користувачів. Flask-Login

## Запуск

```
cd lab9
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python setup_db.py        # міграція + БД
python shell_demo.py      # п.2: хешований пароль (скрін)
python run.py             # http://127.0.0.1:5000
pytest -v                 # п.8: тести (скрін)
```

## Відповідність завданню

| Пункт | Де |
|---|---|
| 1 Flask-Bcrypt | `app/__init__.py` (`bcrypt = Bcrypt()`, `bcrypt.init_app(app)`) |
| 2 хеш пароля у shell | `python shell_demo.py` |
| 3 реєстрація, валідатори | `app/users/forms.py`, `routes.py` (`/register`) |
| 4 вхід з перевіркою хешу | `routes.py` (`/login`), `models.py` (`hash_password`, `check_password`) |
| 5 список користувачів | `/users`, `templates/users.html` |
| 6 Flask-Login | `login_manager`, `user_loader`, `UserMixin`, `login_user`, `logout_user`, `@login_required`, `/account` |
| 7 редирект авторизованих, меню | `register()`/`login()` + `templates/base.html` |
| 8 тести | `tests/` |

## Скріни для звіту

1. **П.2** - вивід `python shell_demo.py` (пароль до/після хешування, `check` True/False).
   Також таблиця `users` у DB Browser for SQLite (`instance/data.sqlite`) із хешем у колонці password.
2. **П.3** - `/register`: помилка для вже існуючого email/username та успішна реєстрація (flash).
3. **П.4, 6** - форма входу, потім сторінка `/account` з даними користувача, кнопка Logout.
4. **П.5** - `/users` зі списком і кількістю (потрібно кілька користувачів: зареєструйте 3-4).
5. **П.6** - спроба відкрити `/account` без входу: перенаправлення на `/login` з повідомленням
   "Please log in to access this page."
6. **П.7** - меню до входу (Login, Register) і після входу (Users, Account, Logout).
7. **П.8** - вивід `pytest -v` (усі тести passed).
