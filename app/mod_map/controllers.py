from flask import render_template, Blueprint

mod_map = Blueprint('map', __name__, url_prefix='/map')

# rendering the map


@mod_map.route('/', methods=['GET'])
def map():
    return render_template("map/map.html")
