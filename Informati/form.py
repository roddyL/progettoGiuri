from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo



'''
Registrazione:
username
email
password
confirm_password
Login:
email
password
remembre_me
'''


class RegistrationForm(FlaskForm):

    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=5, max=100), DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[Length(min=8, max=100),
                                                 DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register Now!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=5, max=100), DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')