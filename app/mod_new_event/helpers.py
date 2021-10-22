from datetime import timedelta, datetime
from flask import session


def datetime_parser(date, time):
    "Time in format HH:MM and date in format yy-mm-dd"
    time = time.split(":")  # nopep8 # splitting starting and ending time with : separator
    timedelta_object = timedelta(hours=int(time[0]),
                                 minutes=int(time[1]))
    datetime_object = datetime(
        date.year, date.month, date.day) + timedelta_object
    return datetime_object


def google_maps_geocode_parser(geocode):
    address = {}

    # lat and lng coordinates
    location = geocode["geometry"]["location"]
    address["lat"] = location["lat"]
    address["lng"] = location["lng"]

    # if there are address components
    address_components = geocode["address_components"]
    if address_components:
        # street name
        address["street_name"] = next(
            (detail["long_name"] for detail in address_components if "route" in detail["types"]), "")

        # street number
        address["street_number"] = next(
            (detail["long_name"] for detail in address_components if "street_number" in detail["types"]), "")

        # city
        address["city"] = next(
            (detail["long_name"] for detail in address_components if "locality" in detail["types"]), "")

        # postal code
        address["postal_code"] = next(
            (detail["long_name"] for detail in address_components if "postal_code" in detail["types"]), "")

        # country
        address["country"] = next(
            (detail["long_name"] for detail in address_components if "country" in detail["types"]), "")

    return address


def event_from_session_to_dictionary():
    # dict object that the function returns
    event_dict = {}

    # user_id for event
    event_dict["user_id"] = session.get("user_id")

    event_dict["event_name"] = session.get("event_name")
    event_dict["event_description"] = session.get("event_description")

    # event_address
    session_address = session.get("address")
    event_dict["lat"] = session_address["lat"]
    event_dict["lng"] = session_address["lng"]
    event_dict["street_name"] = session_address["street_name"]
    event_dict["street_number"] = session_address["street_number"]
    event_dict["city"] = session_address["city"]
    event_dict["postal_code"] = session_address["postal_code"]
    event_dict["country"] = session_address["country"]

    # datetimes from start and end times

    session_time_information = session.get("time_information")

    starting_date = datetime.strptime(
        session_time_information["starting_date"], "%Y-%m-%d")
    starting_time = session_time_information["starting_time"]
    starting_datetime = datetime_parser(starting_date, starting_time)

    ending_date = datetime.strptime(
        session_time_information["ending_date"], "%Y-%m-%d")
    ending_time = session_time_information["ending_time"]
    ending_datetime = datetime_parser(ending_date, ending_time)

    # datetimes to unix
    event_dict["starting_datetime_unix"] = int(starting_datetime.timestamp())
    event_dict["ending_datetime_unix"] = int(ending_datetime.timestamp())

    # capacity
    event_dict["capacity"] = session.get("capacity")

    return event_dict


def clear_event_session():
    session.pop("event_name", None)
    session.pop("event_description", None)
    session.pop("address", None)
    session.pop("time_information", None)
    session.pop("capacity", None)
