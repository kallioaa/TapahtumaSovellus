from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object("config")
Bootstrap(app)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


from app.mod_auth.controllers import mod_auth  # nopep8

app.register_blueprint(mod_auth)
