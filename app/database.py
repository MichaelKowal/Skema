'''
This class initializes the database in the
schema.sql file.  It is called by the __init__
class when first setting up the app and is called
upon session completion to close the database
'''


import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_database():
    if 'database' not in g:
        g.database = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row

    return g.database

def close_database(e=None):
    database = g.pop('database', None)

    if database is not None:
        database.close()

def init_database():
    database = get_database()
    with current_app.open_resource('schema.sql') as f:
        database.executescript(f.read().decode('utf8'))

@click.command('init_database')
@with_appcontext
def init_database_command():
    init_database()
    click.echo('Initialized the database')

def init_app(app):
    app.teardown_appcontext(close_database)
    from . import parser
    file = 'sample_data_2017.csv'
    parser.parse(file)
    app.cli.add_command(init_database_command)
