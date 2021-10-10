from flask import render_template, Blueprint
from flask_googlemaps import Map

mod_map = Blueprint('map', __name__, url_prefix='/map')

# rendering the map


@mod_map.route('/', methods=['GET'])
def map_view():
    # creating a map in the view
    map = Map(
        identifier="view-side",
        lat=60.192059,
        lng=24.945831
    )
    return render_template('map/map.html', map=map)
