'''Defines login and registration form objects'''
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):
    '''Login form class'''
    # no validators other than data required
    # because length/complexity validation happens while registering
    username = TextAreaField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    '''Registration form class'''
    username = TextAreaField("Username", [
        validators.DataRequired(),
        validators.regexp(
            "^[a-zA-Z0-9]{8,}$",
            message="Username must be at least 8 characters "
            "and contain only digits and uppercase/lowercase letters"
        )])
    password = PasswordField("Enter Password", [
        validators.DataRequired(),
        validators.regexp(
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{12,}$",
            message="Password must be at least 12 characters "
            "and contain at least 1 lowercase letter, 1 uppercase letter, 1 digit,"
            "and 1 special character"
        ),
        # passwords must match
        validators.EqualTo("password2", message="Passwords must match")
    ])
    # confirm password before registration
    password2 = PasswordField("Confirm Password")
    submit = SubmitField("Register")
