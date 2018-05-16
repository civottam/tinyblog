from flask_wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Length
import re
from wtforms import ValidationError


class CommentForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    text = TextField(u'Comment', validators=[DataRequired()])


def custom_email(form_object, field_object):
    if not re.match(r"[^@+@[^@]+\.[^@]]+", field_object.data):
        raise ValidationError("Field must be a valid email address!")