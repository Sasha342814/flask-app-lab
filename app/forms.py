from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional

TOPICS = [
    ('', '— Оберіть тему —'),
    ('question', 'Питання'),
    ('cooperation', 'Співпраця'),
    ('bug', 'Повідомити про помилку'),
    ('other', 'Інше'),
]


class ContactForm(FlaskForm):
    name = StringField('Ім\'я', validators=[
        DataRequired(message='Вкажіть ім\'я.'),
        Length(min=2, max=50, message='Ім\'я має містити від 2 до 50 символів.'),
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Вкажіть email.'),
        Email(message='Некоректна адреса електронної пошти.'),
    ])
    phone = StringField('Телефон (необов\'язково)', validators=[
        Optional(),
        Regexp(r'^\+?[0-9 ()\-]{7,20}$', message='Некоректний номер телефону.'),
    ])
    topic = SelectField('Тема', choices=TOPICS, validators=[
        DataRequired(message='Оберіть тему звернення.'),
    ])
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(message='Напишіть повідомлення.'),
        Length(min=10, max=1000, message='Повідомлення має містити від 10 до 1000 символів.'),
    ])
    submit = SubmitField('Надіслати')
