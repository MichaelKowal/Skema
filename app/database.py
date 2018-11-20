'''
This class initializes the database in the
schema.sql file.  It is called by the __init__
class when first setting up the app and is called
upon session completion to close the database
'''


import sqlite3
from . import log
import click
from flask import current_app, g
from flask.cli import with_appcontext
import pandas
import json


def get_db():
    if 'database' not in g:
        g.database = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row

    return g.database


def close_db(e=None):
    db = g.pop('database', None)

    if db is not None:
        db.close()


'''
Take in a file and a name and create or replace a table with that name.  Before the table is created, reduce 
dimensionality by combining the pattern datetimes and the standard datetimes and removing the former from the 
data set.
'''


def fill_db(semester, file):
    from pandas.compat import FileNotFoundError
    try:
        df = pandas.read_csv(file)
    except FileNotFoundError as e:
        log.add_event(str(e))
        print(str(e))
        exit()
    df.columns = ['title', 'component_id', 'start_date', 'end_date', 'day',
                  'start_time', 'duration', 'pattern_day', 'pattern_start_time',
                  'pattern_duration', 'building_id', 'room_number', 'professor']
    df.index.name = 'crn'
    df = df.dropna(thresh=8)
    df = df.fillna('')
    df['day'] = df[['day', 'pattern_day']].apply(lambda x: ''.join(x.map(str)), axis=1)
    lst = []
    for index, row in df.iterrows():
        if str(row['day']) == 'Monday':
            lst.append('2018-01-01')
        if str(row['day']) == 'Tuesday':
            lst.append('2018-01-02')
        if str(row['day']) == 'Wednesday':
            lst.append('2018-01-03')
        if str(row['day']) == 'Thursday':
            lst.append('2018-01-04')
        if str(row['day']) == 'Friday':
            lst.append('2018-01-05')
        if str(row['day']) == 'Saturday':
            lst.append('2018-01-06')
        if str(row['day']) == 'Sunday':
            lst.append('2018-01-07')
    df['date'] = lst
    df['start_time'] = df[['start_time', 'pattern_start_time']].apply(lambda x: ''.join(x.map(str)), axis=1) + ':00'
    df['duration'] = df[['duration', 'pattern_duration']].apply(lambda x: ''.join(x.map(str)), axis=1) + ':00'
    df['start'] = df[['date', 'start_time']].apply(lambda x: 'T'.join(x.map(str)), axis=1)
    df['end'] = pandas.to_datetime(df['start_time']) + pandas.to_timedelta(df['duration'])
    df['end'] = df['end'].dt.time
    df['end'] = df[['date', 'end']].apply(lambda x: 'T'.join(x.map(str)), axis=1)
    df = df.drop(['start_date', 'end_date', 'day', 'start_time', 'duration','pattern_day', 'pattern_start_time',
                  'pattern_duration', 'building_id', 'date', ], 1)
    conn = sqlite3.connect('instance/skemaDB.sqlite')
    df.to_sql(semester, conn, if_exists='replace')
    conn.commit()
    print('database updated!')



def get_events(semester):
    db = get_db()
    cursor = db.cursor()
    statement = 'SELECT * FROM ' + semester
    data = cursor.execute(statement).fetchall()
    classes = [dict(zip([key[0] for key in cursor.description], row)) for row in data]
    return str(json.dumps(({'classes': classes})))


def get_classes(semester, subject, prof, years):
    db = get_db()
    cursor = db.cursor()
    if subject == 'Subject':
        subject = '____'
    if prof == "Instructor":
        prof = '%'
    if len(years) == 1:
        statement = 'SELECT * FROM ' + semester+ ' WHERE ' \
                    'professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[0]) + '%\''
    elif len(years) == 2:
        statement = 'SELECT * FROM ' + semester + ' WHERE ' \
                        'professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[0]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[1]) + '%\''
    elif len(years) == 3:
        statement = 'SELECT * FROM ' + semester + ' WHERE ' \
                        'professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[0]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[1]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[2]) + '%\''
    elif len(years) == 4:
        statement = 'SELECT * FROM ' + semester + ' WHERE ' \
                        'professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[0]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[1]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[2]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[3]) + '%\''
    elif len(years) == 4:
        statement = 'SELECT * FROM ' + semester + ' WHERE ' \
                        'professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[0]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[1]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[2]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[3]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[4]) + '%\''
    elif len(years) == 4:
        statement = 'SELECT * FROM ' + semester + ' WHERE ' \
                        'professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[0]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[1]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[2]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[3]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[4]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[5]) + '%\''
    elif len(years) == 4:
        statement = 'SELECT * FROM ' + semester + ' WHERE ' \
                        'professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[0]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[1]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[2]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[3]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[4]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[5]) + '%\'' + \
                    ' OR professor LIKE \'' + prof + '\' AND title LIKE \'' + subject + str(years[6]) + '%\''
    else:
        statement = 'SELECT * FROM ' + semester + ' WHERE title LIKE \'' + subject \
                    + '%\' AND professor LIKE \'' + prof + '\''
    data = cursor.execute(statement).fetchall()
    classes = [dict(zip([key[0] for key in cursor.description], row)) for row in data]
    return str(json.dumps(({'classes': classes})))


def get_profs(semester):
    db = get_db()
    cursor = db.cursor()
    statement = 'SELECT DISTINCT professor FROM ' + semester + ' ORDER BY professor'
    rows = cursor.execute(statement).fetchall()
    lst = []
    for row in rows:
        if sum(1 for c in row[0] if c.isupper()) < 4 and row[0] != '':
            lst.append(row[0])
    return lst


def get_subject(semester):
    db = get_db()
    cursor = db.cursor()
    statement = 'SELECT DISTINCT (SUBSTR(title, 0, 5)) FROM ' + semester
    rows = cursor.execute(statement).fetchall()
    lst = []
    for row in rows:
        lst.append(row[0])
    return lst


def get_semesters():
    db = get_db()
    cursor = db.cursor()
    rows = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    lst = []
    for row in rows:
        lst.append(row[0])
    return lst


'''
The following methods are for command line manipulation of the this app.  They are not necessary when working within
the webpage.  

fills the database with a file from the given path.Will throw an error if the file passed is not in the correct format.
'''


@click.command('fill_db')
@click.argument('file')
@click.argument('semester')
@with_appcontext
def fill_db_command(semester, file):
    fill_db(semester, file)
    event = 'Database filled with ' + file
    log.add_event(event)
    click.echo(event)



'''
These are all commands that can be used in the virtual environment.  Call them before calling flask run.
'''


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(fill_db_command)
