from flask_sqlalchemy import SQLAlchemy
from app import app
from os import getenv

db = SQLAlchemy(app)

# create tables from sql schema file if we don't launch in Heroku since it creates concurrency issues

is_prod = getenv('IS_HEROKU', None)
if not is_prod:

    fd = open(app.config.get("SQL_TABLES_SCHEMA"), 'r')
    sql_file = fd.read()
    fd.close()

    # sql commands
    sql_commands = sql_file.split(';')

    # dropping empty commands
    sql_commands = list(filter(None, sql_commands))

    # creating each table
    for command in sql_commands:
        db.session.execute(command + ";")

    db.session.commit()
