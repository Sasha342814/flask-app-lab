from flask import render_template, redirect, url_for, flash

from . import app, contact_logger
from .forms import ContactForm, TOPICS


@app.route('/')
def home():
    return render_template('homepage.html', title='Головна')


@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        topic_label = dict(TOPICS).get(form.topic.data, form.topic.data)
        try:
            contact_logger.info(
                'name=%r | email=%r | phone=%r | topic=%r | message=%r',
                form.name.data, form.email.data, form.phone.data or '-',
                topic_label, form.message.data,
            )
        except OSError:
            flash('Не вдалося зберегти повідомлення. Спробуйте пізніше.', 'danger')
            return redirect(url_for('contact'))
        flash(f'Дякуємо, {form.name.data}! Ваше повідомлення надіслано.', 'success')
        return redirect(url_for('contact'))  # Post/Redirect/Get

    if form.errors:
        flash('Форму не надіслано: виправте помилки у полях.', 'danger')
    return render_template('contacts.html', title='Контакти', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Не знайдено'), 404
