from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, regexp


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=4, max=25)], )
    keyword = StringField(label='Keyword:', validators=[Length(min=4, max=25), regexp(regex='^[A-Za-z0-9_-]*$')])
    submit = SubmitField(label='Create Account')
