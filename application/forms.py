from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    keyword = StringField(label='Keyword:')
    submit = SubmitField(label='Create Account')
