from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('BELÉPÉS')


class AddUserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    description = StringField('description')
    contact = StringField('contact')
    password1 = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])
    is_superuser = BooleanField('is_superuser')
