from flask import render_template, redirect, Blueprint, url_for, session
from app.mod_auth.forms import LoginForm, CreateUserForm
from app.mod_auth.models import add_user_to_database, get_user_id
from passlib.hash import pbkdf2_sha256

mod_auth = Blueprint('auth', __name__, url_prefix='/')

# login


@mod_auth.route('/', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        username = form["username"].data
        user_id = get_user_id(username)
        session["user_id"] = user_id
        return redirect(url_for("map.map_view"))
    return render_template("auth/log_in.html", form=form)

# new user creation


@mod_auth.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = CreateUserForm()
    if form.validate_on_submit():  # if true we can safely create a new user
        username = form["username"].data
        password = form["password"].data
        password_hashed = pbkdf2_sha256.hash(password)
        email = form["email"].data
        add_user_to_database(username, password_hashed, email)
        return redirect(url_for(".log_in"))
    return render_template("auth/new_user.html", form=form)


@mod_auth.route("log_out", methods=["GET", "POST"])
def log_out():
    session.pop("user_id", None)
    return redirect(url_for(".log_in"))
