from flask import render_template, Blueprint
from app.mod_map.models import get_events_from_database
from flask_googlemaps import Map
from app.mod_map.helpers import generate_infobox

mod_map = Blueprint('map', __name__, url_prefix='/map')

# rendering the map


@mod_map.route('/', methods=['GET'])
def map_view():
    # creating a map in the view
    events_dict = get_events_from_database()
    markers = [{"lat": event["lat"], "lng": event["lng"], "infobox": generate_infobox(
        event["event_name"], event["event_description"])} for event in events_dict]
    map = Map(
        identifier="view-side",
        lat=60.192059,
        lng=24.945831,
        markers=markers
    )
    return render_template('map/map.html', map=map)
