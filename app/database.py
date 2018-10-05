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

# adds the schedules table to the database.  If a table called
# schedules already exists, it is destroyed and a new one is
# created
def init_database():
    database = get_database()
    with current_app.open_resource('schema.sql') as f:
        database.executescript(f.read().decode('utf8'))

# removes the 'schedules' table from the database
def destroy_database():
    db = get_database()
    db.execute('''DROP TABLE IF EXISTS schedules''')

# prints the requested column
def fetch_database(field):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT ''' + field + ''' FROM schedules''')
    all_rows = cursor.fetchall()
    for row in all_rows:
        print(row[0])

# initialize the database by running "flask init_database" in
# the venv.  It will create a new skemaDB.sqlite file in
# the instance folder
@click.command('init_database')
@with_appcontext
def init_database_command():
    init_database()
    click.echo('Initialized the database')

# returns any column passed in as an argument.
# For Example: 'flask fetch_database course_id'
# will return all of the course ids in the database
@click.command('fetch_database')
@click.argument('field')
@with_appcontext
def fetch_database_command(field):
    click.echo('Data: \n')
    fetch_database(field)

# fills the database with a file from the given path.
# Will throw an error if the file passed is not in
# the correct format.
@click.command('fill_database')
@click.argument('filePath')
@with_appcontext
def fill_database_command(filePath):
    from . import parser
    parser.parse(filePath)

# drops the table from the database, removing everything
# in it.
@click.command('destroy_database')
@with_appcontext
def destroy_database_command():
    destroy_database()
    click.echo('Database destroyed')

# these are all commands that can be used in the virtual
# environment.  Call them before calling flask run.
def init_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_database_command)
    app.cli.add_command(fill_database_command)
    app.cli.add_command(destroy_database_command)
    app.cli.add_command(fetch_database_command)
