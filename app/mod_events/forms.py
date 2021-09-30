from itertools import starmap
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import InputRequired, ValidationError


class NewEventForm(FlaskForm):
    name = StringField("name", validators=[InputRequired()])
    address = StringField("address", validators=[InputRequired()])
    starting_time = DateTimeField("starting time")
    ending_time = DateTimeField("ending time")
    submit = SubmitField('Create Event', validators=[])
