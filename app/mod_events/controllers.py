from operator import add
from flask import render_template, redirect, Blueprint, url_for, session
from flask_googlemaps import Map
from app.mod_events.forms import NameForm, AddressForm, StartAndEndTimeForm, ConfirmAddressForm


mod_events = Blueprint('events', __name__, url_prefix='/events')


@mod_events.route('/new_event_name', methods=['GET', 'POST'])
def new_event_name():
    form = NameForm()
    if form.validate_on_submit():
        session["event_name"] = form["event_name"].data
        return redirect(url_for(".new_event_address"))
    return render_template("general/basic_form.html", form=form, title="New event name")


@mod_events.route('/new_event_address', methods=['GET', 'POST'])
def new_event_address():
    if not session.get("event name"):
        redirect(url_for(".new_event_name"))
    title = "New event address"
    address_form = AddressForm()
    confirm_address_form = ConfirmAddressForm()
    if address_form.validate_on_submit():
        lat = address_form.meta["lat"]
        lng = address_form.meta["lng"]
        map = Map(
            identifier="view-side",
            lat=lat,
            lng=lng,
            markers=[(lat, lng)]
        )
        return render_template("events/address_form.html", address_form=address_form, confirm_address_form=confirm_address_form, map=map, title=title)
    if confirm_address_form.validate_on_submit():
        session["lat"] = address_form.meta["lat"]
        session["let"] = address_form.meta["lng"]
        return render_template(url_for(".new_event_start_and_end_time"))
    return render_template("events/address_form.html", address_form=address_form, title=title)


@mod_events.route('/new_event_start_and_end_time', methods=['GET', 'POST'])
def new_event_start_and_end_time():
    form = StartAndEndTimeForm()
    return render_template("general/basic_form.html", form=form, title="New event start and end")
