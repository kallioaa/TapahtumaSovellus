from flask import render_template, Blueprint
from app.mod_auth.forms import LoginForm, CreateUserForm
from app.mod_auth.models import *

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# login


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("auth/login.html", form=form)

# new user creation


@mod_auth.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = CreateUserForm()
    return render_template("auth/new_user.html", form=form)
