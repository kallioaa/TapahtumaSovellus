from flask import config
from flask_sqlalchemy import SQLAlchemy
from app import app
from os import getenv

db = SQLAlchemy(app)

# create tables from sql schema file if we don't launch in Heroku since it creates concurrency issues

is_prod = getenv('IS_HEROKU', None)
if not is_prod:

    fd = open(app.config.get("SQL_TABLES_SCHEMA"), 'r')
    sqlFile = fd.read()
    fd.close()

    # sql commands
    sqlCommands = sqlFile.split(';')

    # dropping empty commands
    sqlCommands = list(filter(None, sqlCommands))

    # creating each table
    for command in sqlCommands:
        db.session.execute(command + ";")

    db.session.commit()
