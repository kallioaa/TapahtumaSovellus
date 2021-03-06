from app.nav_bar import nav
from flask import Flask, render_template
import googlemaps
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from os import getenv

app = Flask(__name__)

# takes variables from config file if not ran in heroku
is_prod = getenv('IS_HEROKU', None)

if is_prod:
    app.secret_key = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQL_TABLES_SCHEMA"] = getenv("SQL_TABLES_SCHEMA")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")  # nopep8
    app.config["GOOGLEMAPS_KEY"] = getenv("GOOGLEMAPS_KEY")
else:
    app.config.from_object("config")

Bootstrap(app)
GoogleMaps(app)  # for maps
gmaps = googlemaps.Client(key=app.config.get("GOOGLEMAPS_KEY"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


# initalize navbar
nav.init_app(app)

from app.mod_auth.controllers import mod_auth  # nopep8
from app.mod_map.controllers import mod_map  # nopep8
from app.mod_new_event.controllers import mod_new_event  # nopep8

app.register_blueprint(mod_auth)
app.register_blueprint(mod_map)
app.register_blueprint(mod_new_event)
