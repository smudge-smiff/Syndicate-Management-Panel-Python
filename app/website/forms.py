from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
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

class CreateAGroupForm(FlaskForm):
    groupname = StringField("Group Name:", validators=[DataRequired(), Length(min=5, max=40)])
    
class JoinAGroupForm(FlaskForm):
    jointoken = StringField("Join Token:", validators=[DataRequired(), Length(min=12, max=12)])

class CreateAssetForm(FlaskForm):
    assetname = StringField("Asset Name:", validators=[DataRequired(), Length(min=2, max=150)])
    type = SelectField("Asset Type:", choices = [('airplane', 'Airplane'), ('boat', 'Boat'), ('car', 'Car')], validators=[DataRequired()])