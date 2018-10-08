from app.database import get_database
import click

# parses a .csv that is passed to it.  Creates an array with
# the data
def parse(file):
    file_contents_by_row = []
    last_line = None
    with open(file) as sample_file:
        for line in sample_file:
            if not last_line:
                row = line.split(",")
                file_contents_by_row.append(row)
    if len(file_contents_by_row[0]) is not 13:
        click.echo('ERROR: csv is not in correct format')
        return
    fill_database(file_contents_by_row)


# fills the database with an array that is passed with it
def fill_database(file_contents_by_row):

    # use this a placeholder for the crn
    crn = 0

    db = get_database()

    for x in file_contents_by_row[4: ]:
        db.execute('''INSERT INTO schedules(crn, course_id, component_id, start_date, end_date, day, start_time, duration,
            pattern_day, pattern_start_time, pattern_duration, building_id, room_number, professor) VALUES(?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?)''', (crn, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12]))
        crn += 1
    db.commit()
    click.echo('database filled')

