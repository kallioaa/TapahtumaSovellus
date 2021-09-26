CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS admin (
    user_id INTEGER REFERENCES users
);