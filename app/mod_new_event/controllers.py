from datetime import datetime
from app.mod_new_event.models import add_event_to_database
from flask import render_template, redirect, Blueprint, url_for, session, request
from flask_googlemaps import Map
from app.mod_new_event.forms import NameForm, AddressForm, StartAndEndTimeForm, EventDetailsForm
from app.mod_new_event.helpers import google_maps_geocode_parser, event_from_session_to_dictionary, clear_event_session


mod_new_event = Blueprint('new_event', __name__, url_prefix='/new_event')


@mod_new_event.route('/new_event_name', methods=['GET', 'POST'])
def new_event_name():
    if not session.get("user_id"):
        return redirect(url_for("auth.log_in"))
    form = NameForm()

    # if there is a session value we use it
    if request.method == "GET":
        session_event_name = session.get("event_name")
        if session_event_name:
            form.event_name.data = session_event_name
        session_event_description = session.get("event_description")
        if session_event_description:
            form.event_description.data = session_event_description

    if request.method == "POST":
        if form.validate_on_submit():
            session["event_name"] = form["event_name"].data
            session["event_description"] = form["event_description"].data
            return redirect(url_for(".new_event_address"))
    return render_template("general/basic_form.html", form=form, title="New event name")


@mod_new_event.route('/new_event_address', methods=['GET', 'POST'])
def new_event_address():
    if not session.get("user_id"):
        return redirect(url_for("auth.log_in"))
    if not session.get("event_name"):
        return redirect(url_for(".new_event_name"))
    title = "New event address"
    form = AddressForm()

    # if there is an address in the session we use it
    if request.method == "GET":
        session_address = session.get("address")
        if session_address:
            form.address.data = '{} {} {} {} {}'.format(
                session_address["street_name"], session_address["street_number"], session_address["city"], session_address["postal_code"], session_address["country"])

    if request.method == "POST":
        if form.validate_on_submit():  # if search address button is pressed
            # lat and lng coordinates

            geocode = form.meta
            address = google_maps_geocode_parser(geocode)
            map = Map(
                identifier="view-side",
                lat=address["lat"],
                lng=address["lng"],
                markers=[(address["lat"], address["lng"])]
            )
            session["address"] = address
            return render_template("new_event/address_form.html", form=form, map=map, title=title)
    return render_template("new_event/address_form.html", form=form, title=title)


@mod_new_event.route('/new_event_start_and_end_time', methods=['GET', 'POST'])
def new_event_start_and_end_time():
    if not session.get("user_id"):
        return redirect(url_for("auth.log_in"))
    if not session.get("address"):
        return redirect(url_for(".new_event_address"))
    form = StartAndEndTimeForm()
    # if there is an address in the session we use it
    if request.method == "GET":
        session_time_information = session.get("time_information")
        if session_time_information:
            form.starting_date.data = datetime.strptime(
                session_time_information["starting_date"], "%Y-%m-%d")
            form.starting_time.data = session_time_information["starting_time"]
            form.ending_date.data = datetime.strptime(
                session_time_information["ending_date"], "%Y-%m-%d")
            form.ending_time.data = session_time_information["ending_time"]

    if request.method == "POST":
        if form.validate_on_submit():
            time_information = {}

            # create starting datetime
            time_information["starting_date"] = form["starting_date"].data.strftime(
                "%Y-%m-%d")
            time_information["starting_time"] = form["starting_time"].data

            # create ending datetime
            time_information["ending_date"] = form["ending_date"].data.strftime(
                "%Y-%m-%d")
            time_information["ending_time"] = form["ending_time"].data

            session["time_information"] = time_information

            return redirect(url_for(".new_event_details"))
    return render_template("general/basic_form.html", form=form, title="New event start and end")


@mod_new_event.route('/new_event_details', methods=['GET', 'POST'])
def new_event_details():
    if not session.get("user_id"):
        return redirect(url_for("auth.log_in"))
    form = EventDetailsForm()
    if request.method == "POST":
        if form.validate_on_submit():
            session["capacity"] = form["capacity"].data
            event_dict = event_from_session_to_dictionary()
            add_event_to_database(event_dict)
            clear_event_session()
            return redirect(url_for("map.map_view"))
    return render_template("general/basic_form.html", form=form, title="New event details")
