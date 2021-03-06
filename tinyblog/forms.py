import re
from flask_wtf import Form, RecaptchaField, FlaskForm
from wtforms import StringField, TextField, TextAreaField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, URL

from tinyblog.models import User


class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Blog Content', [DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember me')

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False
        # check if user exists
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False
        # check if password is correct
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            return False
        return True


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    text = TextField(u'Comment', validators=[DataRequired()])


def custom_email(form_object, field_object):
    if not re.match(r"[^@+@[^@]+\.[^@]]+", field_object.data):
        raise ValidationError("Field must be a valid email address!")