from flask import Blueprint, render_template, request, redirect, url_for

users_bp = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')


@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', type=int)
    return render_template('users/hi.html', title='Привітання', name=name, age=age)


@users_bp.route('/admin')
def admin():
    # Приклад редіректу: /users/admin -> /users/hi/administrator?age=45
    return redirect(url_for('users.greetings', name='administrator', age=45))
