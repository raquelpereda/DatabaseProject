from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    firstname = StringField("First Name",
                            validators=[DataRequired(), Length(max=20)])
    lastname = StringField("Last Name",
                            validators=[DataRequired(), Length(max=20)])                            
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                        validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                        validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")