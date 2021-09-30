from flask import render_template, redirect, Blueprint
from app.mod_events.forms import NewEventForm


mod_events = Blueprint('events', __name__, url_prefix='/events')


@mod_events.route('/new_event', methods=['GET', 'POST'])
def new_event():
    form = NewEventForm()
    return render_template("events/new_event.html", form=form)
