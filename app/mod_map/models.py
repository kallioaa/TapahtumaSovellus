from app.db import db


def get_events_from_database():
    sql = "SELECT event_name, event_description, lat, lng, starting_datetime_unix, ending_datetime_unix  FROM events"
    result = db.session.execute(sql)
    events = result.fetchall()
    events_dict = [{"event_name": event[0], "event_description": event[1],
                    "lat": event[2], "lng": event[3], "starting_datetime_unix": event[3], "ending_datetime_unix": event[4]} for event in events]
    return events_dict
