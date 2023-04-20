"""py-file with user wtforms"""


from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, EmailField, BooleanField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """form for login with next fields
    email (required)
    password (required)"""
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class EditForm(FlaskForm):
    """form for editing a user with next fields
    nick (nickname, required)
    email (required)
    password (required)"""
    nick = StringField('Nickname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Edit')


class SigninForm(FlaskForm):
    """form for signin with next fields
    nick (nickname, required)
    email (required)
    password (required)
    password_again (required)"""
    nick = StringField('Nickname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    submit = SubmitField('Sign in')
