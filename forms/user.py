from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
