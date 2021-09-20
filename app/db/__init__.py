from flask import config
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

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
