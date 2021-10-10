from datetime import datetime, timedelta, date
from flask import session
from flask.app import Flask
from app import gmaps
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import InputRequired, ValidationError


def validate_address(form, field):
    address = form["address"].data
    coordinates = gmaps.geocode(address)
    if not coordinates:
        session.pop("event_address", None)
        form.meta = None
        raise ValueError("Address not found")
    form.meta = coordinates[0]["geometry"]["location"]


class NameForm(FlaskForm):
    event_name = StringField("Event name", validators=[InputRequired()])
    submit = SubmitField('Confirm Name', validators=[])


class AddressForm(FlaskForm):
    address = StringField("address", validators=[
                          InputRequired()])
    submit = SubmitField("Search address", validators=[validate_address])


class ConfirmAddressForm(FlaskForm):
    submit = SubmitField("Confirm address", validators=[validate_address])


class StartAndEndTimeForm(FlaskForm):
    def _generate_times_list(starting_date):

        def _datetime_range(start, end, delta):
            current = start
            while current < end:
                yield current
                current += delta

        # if the date is not the same we will show every slot
        times_list = [dt.strftime('%H:%M') for dt in
                      _datetime_range(datetime.combine(date.today(), datetime.min.time()), datetime.combine(date.today() + timedelta(days=1), datetime.min.time()),
                      timedelta(minutes=15))]
        return times_list

    starting_date = DateField("starting date", default=datetime.today)
    starting_time = SelectField(
        "starting time", choices=_generate_times_list(starting_date))
    ending_date = DateField("ending date", default=datetime.today)
    ending_time = SelectField("ending time")
    submit = SubmitField('Create Event', validators=[])
