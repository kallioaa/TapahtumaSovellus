CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS admins (
    user_id INTEGER REFERENCES users
);
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    event_name TEXT,
    event_description TEXT,
    lat REAL,
    lng REAL,
    street_name TEXT,
    street_number TEXT,
    city TEXT,
    postal_code TEXT,
    country TEXT,
    starting_datetime_unix INTEGER,
    ending_datetime_unix INTEGER,
    capacity INTEGER
);