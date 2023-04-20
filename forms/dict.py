"""py-file with dictionary wtforms"""


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class AddDictForm(FlaskForm):
    """form for adding a new dict with next fields
    title (required)
    desc (description, not required)
    words (not required)
    is_pb (is_public, not required)"""
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Description')
    words = SelectMultipleField('Words', choices=[])
    is_pb = BooleanField('Is public')
    submit = SubmitField('Add')


class EditDictForm(FlaskForm):
    """form for editing a dict with next fields
    title (required)
    desc (description, not required)
    words (not required)
    is_pb (is_public, not required)"""
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Description')
    words = SelectMultipleField('Words', choices=[])
    is_pb = BooleanField('Is public')
    submit = SubmitField('Edit')
