from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, EmailField, BooleanField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class EditForm(FlaskForm):
    nick = StringField('Nickname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Edit')


class SigninForm(FlaskForm):
    nick = StringField('Nickname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    submit = SubmitField('Sign in')
