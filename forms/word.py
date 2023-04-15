from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    tr_list = TextAreaField('Translation', validators=[DataRequired()])
    is_pb = BooleanField('Is public', validators=[DataRequired()])
    submit = SubmitField('Add')
