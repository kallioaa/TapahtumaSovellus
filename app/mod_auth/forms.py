from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email
from app.mod_auth.models import username_exists, email_exists, check_login_authorized

# checks if username and email are available


def validate_username_taken(form, field):
    username = form["username"]
    if username_exists(username.data):
        username_taken_error = ValidationError("Username taken!")
        username.errors.append(username_taken_error)
        raise username_taken_error


def validate_email_taken(form, field):
    email = form["email"]
    if email_exists(email.data):
        email_taken_error = ValidationError("Email is taken!")
        email.errors.append(email_taken_error)
        raise email_taken_error


def validate_username_not_existing(form, field):
    username = form["username"]
    if not username_exists(username.data):
        username_taken_error = ValidationError("Username does not exist!")
        username.errors.append(username_taken_error)
        raise username_taken_error


def validate_login_authorized(form, field):
    username = form["username"]
    if not username.errors:  # if username field does not contain validation errors we try to login
        password = form["password"]
        if not check_login_authorized(username.data, password.data):
            password_incorrect_error = ValidationError(
                "Password is incorrect!")
            password.errors.append(password_incorrect_error)
            raise password_incorrect_error


class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(
        min=3, max=20, message="Username length between 3 and 20 characters!")])
    password = PasswordField("password", validators=[InputRequired(), Length(
        min=3, max=50, message="Password length between 3 and 50 characters!")])
    submit = SubmitField('Login', validators=[
                         validate_username_not_existing, validate_login_authorized])


class CreateUserForm(FlaskForm):
    username = StringField("username", validators=[
                           InputRequired(), Length(min=3, max=20, message="Username length between 3 and 20 characters!")])
    password = PasswordField("password", validators=[
                             InputRequired(), Length(min=3, max=50, message="Password length between 3 and 50 characters!")])
    password_repeat = PasswordField("password repeat", validators=[
                                    InputRequired(), EqualTo("password", message="Passwords do not match")])
    email = StringField("email", validators=[
                        InputRequired(), Email(granular_message=True)])
    submit = SubmitField("Create new user", validators=[
                         validate_username_taken, validate_email_taken])
