from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, SelectField, SelectMultipleField,
                     StringField, SubmitField, TextAreaField)
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length

CATEGORIES = [("tech", "Tech"), ("lifestyle", "LifeStyle"), ("art", "Art")]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40},
                            validators=[DataRequired()])
    publish_date = DateTimeLocalField("Publish Date", format="%Y-%m-%dT%H:%M",
                                      default=datetime.now)
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    # Пункт 8: вибір автора зі списку з БД
    author_id = SelectField("Author", coerce=int)
    # Пункт 11: вибір кількох тегів
    tags = SelectMultipleField("Tags", coerce=int)
    is_active = BooleanField("Is this post active?", default=True)
    submit = SubmitField("Add Post")
