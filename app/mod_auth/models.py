from app.db import db
from passlib.hash import pbkdf2_sha256

# checks if the usrenam,e exists in the database


def username_exists(username):
    sql = "SELECT COUNT(*) FROM users WHERE username = :username"
    r = db.session.execute(sql, {"username": username})
    count = r.first()[0]
    return bool(count)

# checks if the email exists in the database


def email_exists(email):
    sql = "SELECT COUNT(*) FROM users WHERE email = :email"
    r = db.session.execute(sql, {"email": email})
    count = r.first()[0]
    return bool(count)

# adds a new user to the database


def add_to_database(username, password_hashed, email):
    sql = "INSERT INTO USERS (username, password, email) values (:username, :password, :email)"
    db.session.execute(sql, {"username": username,
                             "password": password_hashed, "email": email})
    db.session.commit()

# checks if the login attempt is successful


def check_login_authorized(username, password):
    sql = "SELECT password FROM users WHERE username = :username"
    r = db.session.execute(sql, {"username": username})
    password_hashed_from_db = r.first()[0]
    correct = pbkdf2_sha256.verify(password, password_hashed_from_db)
    return correct

# gets user id


def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = :username"
    r = db.session.execute(sql, {"username": username})
    id = r.first()[0]
    return id
