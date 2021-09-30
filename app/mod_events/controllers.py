from operator import add
from flask import render_template, redirect, Blueprint, url_for
from flask_googlemaps import Map
from app.mod_events.forms import NameForm, AddressForm, StartAndEndTimeForm


mod_events = Blueprint('events', __name__, url_prefix='/events')


@mod_events.route('/new_event_name', methods=['GET', 'POST'])
def new_event_name():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for(".new_event_address"))
    return render_template("general/basic_form.html", form=form, title="New event name")


@mod_events.route('/new_event_address', methods=['GET', 'POST'])
def new_event_address():
    title = "New event address"
    form = AddressForm()
    if form.validate_on_submit():
        lat = form.meta["lat"]
        lng = form.meta["lng"]
        map = Map(
            identifier="view-side",
            lat=lat,
            lng=lng,
            markers=[(lat, lng)]
        )
        return render_template("events/address_form.html", form=form, map=map, title=title)
    return render_template("general/basic_form.html", form=form, title=title)


@mod_events.route('/new_event_start_and_end_time', methods=['GET', 'POST'])
def new_event_start_and_end_time():
    form = StartAndEndTimeForm()
    return render_template("general/basic_form.html", form=form, title="New event start and end")
