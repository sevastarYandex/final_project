from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, EmailField, BooleanField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


EditForm = LoginForm
EditForm.nick = StringField('Nickname', validators=[DataRequired()])
EditForm.submit = SubmitField('Edit')


SigninForm = EditForm
SigninForm.password_again = PasswordField('Password again', validators=[DataRequired()])
SigninForm.submit = SubmitField('Sign in')
