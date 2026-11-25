from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                Regexp, ValidationError)

from app import db
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=4, max=16),
        Regexp(r"^[A-Za-z][A-Za-z0-9_.]*$",
               message="Username must start with a letter and contain only letters, numbers, dots or underscores."),
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match."),
    ])
    submit = SubmitField("Register")

    # Перевірка унікальності username та email у БД
    def validate_username(self, username):
        user = db.session.scalar(select(User).where(User.username == username.data))
        if user:
            raise ValidationError("Username is already taken.")

    def validate_email(self, email):
        user = db.session.scalar(select(User).where(User.email == email.data))
        if user:
            raise ValidationError("Email is already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
