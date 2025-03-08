# This file comes directly from the flask documentaion
# https://flask.palletsprojects.com/en/stable/tutorial/database/
# use the sqlite3 module to connect to the database
import sqlite3
from datetime import datetime

import click
# current app and g create a context for when an app is running
from flask import current_app, g

# create a connection to the database
def get_db():
    # if there is already a connection for this context return the connection,
    # otherwise create a new connection
    if 'db' not in g:
  
        g.db = sqlite3.connect(
            
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # return rows that behave like dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db

# close the database connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# create a new table in the database
def init_db():
    
    db = get_db()
    print("Initializing the database connection")
    with current_app.open_resource('db_schema.sql') as f:
        print("Opening the database schema file")
        try:
            db.executescript(f.read().decode('utf8'))
            print("Database schema created")
        except sqlite3.OperationalError:
            print("Issue with executing the script")
            pass


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)