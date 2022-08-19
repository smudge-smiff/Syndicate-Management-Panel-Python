from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Email Address:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    firstname = StringField("First Name:", validators=[DataRequired(), Length(min=2, max=40)])
    surname = StringField("Surname:", validators=[DataRequired(), Length(min=2, max=40)])
    email = EmailField('Email Address:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords do not match')])
    password_confirm = PasswordField(label='Password confirm', validators=[Length(min=6, max=10)])


