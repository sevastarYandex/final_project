"""py-file with word wtforms"""


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddWordForm(FlaskForm):
    """form for adding a new word with next fields
    word (required)
    tr_list (translation, required)
    is_pb (is_public, not required)"""
    word = StringField('Word', validators=[DataRequired()])
    tr_list = TextAreaField('Translation', validators=[DataRequired()])
    is_pb = BooleanField('Is public')
    submit = SubmitField('Add')


class EditWordForm(FlaskForm):
    """form for editing a word with next fields
    word (required)
    tr_list (translation, required)
    is_pb (is_public, not required)"""
    word = StringField('Word', validators=[DataRequired()])
    tr_list = TextAreaField('Translation', validators=[DataRequired()])
    is_pb = BooleanField('Is public')
    submit = SubmitField('Edit')
