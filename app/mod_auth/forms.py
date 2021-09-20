from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("Log in")


class CreateUserForm(FlaskForm):
    username = StringField("username", validators=[
                           InputRequired(), Length(message="length if off ", min=1, max=25)])
    password = PasswordField("password", validators=[
                             InputRequired(), Length(min=8, max=60)])
    password_repeat = PasswordField("password repeat", validators=[
                                    InputRequired(), EqualTo("password")])
    email = StringField("email", validators=[
                        InputRequired()])
    submit = SubmitField('Create new user')
