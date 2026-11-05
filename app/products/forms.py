from decimal import Decimal

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, AnyOf

CATEGORIES = [
    ('electronics', 'Електроніка'),
    ('clothes', 'Одяг'),
    ('books', 'Книги'),
    ('home', 'Дім і сад'),
    ('other', 'Інше'),
]


def max_two_decimals(form, field):
    """Ціна — не більше двох знаків після коми."""
    if field.data is not None and Decimal(field.data).as_tuple().exponent < -2:
        raise ValidationError('Ціна може мати не більше двох знаків після коми.')


class UkIntegerField(IntegerField):
    """IntegerField з українським повідомленням про нечислове значення."""

    def process_formdata(self, valuelist):
        try:
            super().process_formdata(valuelist)
        except ValueError:
            raise ValueError('Вкажіть ціле число.')


class UkDecimalField(DecimalField):
    """DecimalField з українським повідомленням про нечислове значення."""

    def process_formdata(self, valuelist):
        try:
            super().process_formdata(valuelist)
        except ValueError:
            raise ValueError('Вкажіть ціну числом, наприклад 199.99.')


class ProductForm(FlaskForm):
    name = StringField('Назва', validators=[
        DataRequired(message='Вкажіть назву товару.'),
        Length(min=3, max=100, message='Назва має містити щонайменше 3 символи.'),
    ])
    content = TextAreaField('Опис', render_kw={'rows': 5, 'cols': 40}, validators=[
        DataRequired(message='Вкажіть опис товару.'),
    ])
    price = UkDecimalField('Ціна', places=2, validators=[
        DataRequired(message='Вкажіть ціну (число).'),
        NumberRange(min=Decimal('0.01'), message='Ціна має бути додатною.'),
        max_two_decimals,
    ])
    category = SelectField('Категорія', choices=CATEGORIES, validate_choice=False, validators=[
        AnyOf([key for key, _ in CATEGORIES], message='Оберіть категорію зі списку.'),
    ])
    quantity = UkIntegerField('Кількість', validators=[
        NumberRange(min=0, message='Кількість не може бути від’ємною.'),
    ])
    image = FileField('Зображення', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Дозволені лише файли PNG, JPG, JPEG.'),
    ])
    submit = SubmitField('Зберегти')
