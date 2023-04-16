from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class AddDictForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Description')
    words = SelectMultipleField('Words', choices=[])
    is_pb = BooleanField('Is public')
    submit = SubmitField('Add')


class EditDictForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Description')
    words = SelectMultipleField('Words', choices=[])
    is_pb = BooleanField('Is public')
    submit = SubmitField('Edit')
