from flask_wtf import FlaskForm
from wtforms import (BooleanField,
                     PasswordField,
                     StringField,
                     TextAreaField,
                     SubmitField,
                     EmailField,
                     SelectField)
from wtforms.validators import DataRequired


SEX_CHOICES = [('male', 'male'), ('female', 'female')]


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again',
                                   validators=[DataRequired()])
    name = StringField('User name', validators=[DataRequired()])
    sex = SelectField('User sex', choices=SEX_CHOICES)
    age = StringField('User age', validators=[DataRequired()])
    about = TextAreaField('About yourself')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Enter')
