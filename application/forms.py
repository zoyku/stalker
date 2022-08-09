from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=4, max=25), DataRequired()])
    keyword = StringField(label='Keyword:', validators=[Length(min=4, max=25), Regexp(regex='^[A-Za-z0-9_-]*$'), DataRequired()])
    submit = SubmitField(label='Create Account')
