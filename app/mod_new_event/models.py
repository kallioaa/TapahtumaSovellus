from app.db import db


def add_event_to_database(event_dict):
    sql = "INSERT INTO events(user_id, event_name,event_description, lat, lng, street_name, street_number, city, postal_code, country, starting_datetime_unix, ending_datetime_unix, capacity) VALUES \
        (:user_id, :event_name, :event_description, :lat, :lng, :street_name, :street_number, :city, :postal_code, :country, :starting_datetime_unix, :ending_datetime_unix, :capacity)"
    db.session.execute(sql, event_dict)
    db.session.commit()
