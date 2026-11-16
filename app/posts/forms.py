from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

CATEGORY_CHOICES = [
    ("news", "News"),
    ("publication", "Publication"),
    ("tech", "Tech"),
    ("other", "Other"),
]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField(
        "Content", render_kw={"rows": 5}, validators=[DataRequired()]
    )
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date",
        format="%Y-%m-%dT%H:%M",
        default=datetime.now,
        validators=[Optional()],
    )
    category = SelectField(
        "Category", choices=CATEGORY_CHOICES, validators=[DataRequired()]
    )
    submit = SubmitField("Submit")
