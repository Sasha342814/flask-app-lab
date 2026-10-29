from datetime import timedelta

from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash, make_response)

users_bp = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')

# Заглушка замість бази даних
VALID_USER = {'username': 'admin', 'password': '12345'}
THEMES = ('light', 'dark')


# ---------- Лаба 3 ----------
@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', type=int)
    return render_template('users/hi.html', title='Привітання', name=name, age=age)


@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='administrator', age=45))


# ---------- Лаба 4: автентифікація (сесія) ----------
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == VALID_USER['username'] and password == VALID_USER['password']:
            session['user'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('users.profile'))
        flash('Невірний логін або пароль.', 'danger')
        return redirect(url_for('users.login'))
    return render_template('users/login.html', title='Вхід')


@users_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/profile')
def profile():
    if 'user' not in session:
        flash('Спочатку увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    theme = request.cookies.get('theme', 'light')
    if theme not in THEMES:
        theme = 'light'
    return render_template('users/profile.html', title='Профіль',
                           username=session['user'], theme=theme,
                           cookies=request.cookies)


# ---------- Лаба 4: кукі ----------
def _require_login():
    if 'user' not in session:
        flash('Спочатку увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    return None


@users_bp.route('/cookies/add', methods=['POST'])
def add_cookie():
    denied = _require_login()
    if denied:
        return denied
    key = request.form.get('key', '').strip()
    value = request.form.get('value', '')
    seconds = request.form.get('max_age', type=int)
    if not key:
        flash('Ключ кукі не може бути порожнім.', 'danger')
        return redirect(url_for('users.profile'))
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie(key, value, max_age=seconds if seconds and seconds > 0 else None)
    flash(f'Кукі «{key}» додано.', 'success')
    return resp


@users_bp.route('/cookies/delete', methods=['POST'])
def delete_cookie():
    denied = _require_login()
    if denied:
        return denied
    key = request.form.get('key', '').strip()
    if key not in request.cookies:
        flash(f'Кукі «{key}» не знайдено.', 'warning')
        return redirect(url_for('users.profile'))
    resp = make_response(redirect(url_for('users.profile')))
    resp.delete_cookie(key)
    flash(f'Кукі «{key}» видалено.', 'success')
    return resp


@users_bp.route('/cookies/delete-all', methods=['POST'])
def delete_all_cookies():
    denied = _require_login()
    if denied:
        return denied
    resp = make_response(redirect(url_for('users.profile')))
    for key in request.cookies:
        if key != 'session':  # сесію не чіпаємо, щоб не розлогінити користувача
            resp.delete_cookie(key)
    flash('Усі кукі (крім сесійної) видалено.', 'success')
    return resp


# ---------- Лаба 4: кольорова схема ----------
@users_bp.route('/theme/<string:name>')
def set_theme(name):
    denied = _require_login()
    if denied:
        return denied
    if name not in THEMES:
        flash('Невідома кольорова схема.', 'danger')
        return redirect(url_for('users.profile'))
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('theme', name, max_age=int(timedelta(days=365).total_seconds()))
    flash(f'Схему змінено на «{name}».', 'success')
    return resp
