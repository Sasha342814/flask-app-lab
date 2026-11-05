import os
import uuid
from decimal import Decimal

from flask import (Blueprint, render_template, redirect, url_for, flash,
                   abort, current_app)
from werkzeug.exceptions import RequestEntityTooLarge

from . import db
from .forms import ProductForm, CATEGORIES

products_bp = Blueprint('products', __name__, template_folder='templates',
                        static_folder='static', url_prefix='/product')

CATEGORY_NAMES = dict(CATEGORIES)


# ---------- допоміжні функції ----------
def upload_dir():
    folder = current_app.config.get('UPLOAD_FOLDER') or os.path.join(products_bp.root_path, 'static', 'uploads')
    os.makedirs(folder, exist_ok=True)
    return folder


def save_image(file_storage):
    """Зберігає зображення під випадковим UUID-іменем, повертає відносний шлях."""
    ext = os.path.splitext(file_storage.filename)[1].lower()
    filename = f'{uuid.uuid4().hex}{ext}'
    file_storage.save(os.path.join(upload_dir(), filename))
    return f'uploads/{filename}'


def remove_image(rel_path):
    if rel_path:
        path = os.path.join(upload_dir(), os.path.basename(rel_path))
        if os.path.isfile(path):
            os.remove(path)


@products_bp.app_template_global()
def image_url(product):
    """URL зображення товару або заглушка, якщо його немає / файл зник."""
    rel = product.get('image')
    if rel and rel.startswith('images/'):  # зображення, що входять до проєкту (початкові товари)
        if os.path.isfile(os.path.join(products_bp.root_path, 'static', rel)):
            return url_for('products.static', filename=rel)
    elif rel and os.path.isfile(os.path.join(upload_dir(), os.path.basename(rel))):
        return url_for('products.static', filename=rel)
    return url_for('products.static', filename='images/no-image.svg')


@products_bp.app_template_filter('category_name')
def category_name(key):
    return CATEGORY_NAMES.get(key, key)


@products_bp.app_template_filter('dt')
def format_dt(value):
    return value.replace('T', ' ') if value else ''


def get_or_404(product_id):
    product = db.get_by_id(product_id)
    if product is None:
        abort(404)
    return product


# ---------- CRUD ----------
@products_bp.route('/')
def products_list():
    return render_template('products/products.html', title='Товари', products=db.get_all())


@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image = save_image(form.image.data) if form.image.data else None
        db.add({
            'name': form.name.data.strip(),
            'content': form.content.data,
            'price': float(round(form.price.data, 2)),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image,
        })
        flash('Товар успішно додано.', 'success')
        return redirect(url_for('products.products_list'))  # PRG
    if form.errors:
        flash('Не вдалося зберегти товар: виправте помилки у формі.', 'danger')
    return render_template('products/product_form.html', title='Додати товар', form=form, product=None)


@products_bp.route('/<int:product_id>')
def detail_product(product_id):
    product = get_or_404(product_id)
    return render_template('products/detail_product.html', title=product['name'], product=product)


@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = get_or_404(product_id)
    form = ProductForm()
    if form.validate_on_submit():
        data = {
            'name': form.name.data.strip(),
            'content': form.content.data,
            'price': float(round(form.price.data, 2)),
            'category': form.category.data,
            'quantity': form.quantity.data,
        }
        if form.image.data:  # нове зображення замінює старе, інакше лишається попереднє
            data['image'] = save_image(form.image.data)
            remove_image(product.get('image'))
        db.update(product_id, data)
        flash('Зміни збережено.', 'success')
        return redirect(url_for('products.detail_product', product_id=product_id))
    if not form.is_submitted():
        form.name.data = product['name']
        form.content.data = product['content']
        form.price.data = Decimal(str(product['price']))
        form.category.data = product['category']
        form.quantity.data = product['quantity']
    elif form.errors:
        flash('Не вдалося зберегти зміни: виправте помилки у формі.', 'danger')
    return render_template('products/product_form.html', title='Редагувати товар', form=form, product=product)


@products_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = get_or_404(product_id)
    db.delete(product_id)
    remove_image(product.get('image'))
    flash(f'Товар «{product["name"]}» видалено.', 'success')
    return redirect(url_for('products.products_list'))


@products_bp.app_errorhandler(RequestEntityTooLarge)
def file_too_large(error):
    flash('Файл завеликий (максимум 2 МБ).', 'danger')
    return redirect(url_for('products.products_list'))
