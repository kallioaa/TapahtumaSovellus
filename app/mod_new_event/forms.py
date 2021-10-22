from datetime import datetime, timedelta, date
from flask import session
from app import gmaps
from app.mod_new_event.helpers import datetime_parser
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, DateField, SelectField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, ValidationError


def validate_address(form, field):
    address = form["address"].data
    coordinates = gmaps.geocode(address)
    if not coordinates:
        session.pop("event_address", None)
        form.meta = None
        raise ValueError("Address not found")
    form.meta = coordinates[0]

# check that the combination of start datetime (date + time) is before end datetime


def validate_start_and_end_datetimes(form, field):
    starting_date = form["starting_date"].data
    ending_date = form["ending_date"].data
    if starting_date and ending_date:
        # starting datetime object
        starting_time = form["starting_time"].data
        starting_datetime = datetime_parser(starting_date, starting_time)

        # ending datetime object
        ending_time = form["ending_time"].data
        ending_datetime = datetime_parser(ending_date, ending_time)

        # if starting_datetime if before ending datetine raise an error
        if starting_datetime > ending_datetime:
            raise ValidationError("Ending time is before starting time")


# check that the date is given in a correct format


def validate_date_format(form, field):
    if not field.data:
        raise ValidationError("Input date in yyyy-mm-dd")

# check that starting date is the same or before ending date


def validate_starting_and_ending_date(form, field):
    starting_date = form["starting_date"].data
    ending_date = field.data
    if starting_date and ending_date:
        if ending_date < starting_date:
            ending_time_incorrect = ValidationError(
                "Ending date is before starting time!")
            raise ending_time_incorrect


class NameForm(FlaskForm):
    event_name = StringField("Event name", validators=[InputRequired()])
    event_description = TextAreaField(
        "Event description", validators=[InputRequired()])
    submit = SubmitField('Confirm Name', validators=[])


class AddressForm(FlaskForm):
    address = StringField("address", validators=[
                          InputRequired()])
    search_address = SubmitField(
        "Search address", validators=[validate_address])


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

    starting_date = DateField("starting date", default=datetime.today, validators=[
                              validate_date_format])
    starting_time = SelectField(
        "starting time", choices=_generate_times_list(starting_date))
    ending_date = DateField("ending date", default=datetime.today,
                            validators=[validate_date_format, validate_starting_and_ending_date])
    ending_time = SelectField(
        "ending time", choices=_generate_times_list(starting_date), validators=[validate_start_and_end_datetimes])
    submit = SubmitField('Confirm starting and ending times')


class EventDetailsForm(FlaskForm):
    capacity = IntegerField("maximum capacity")
    submit = SubmitField('Create new event')
