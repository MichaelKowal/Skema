import sqlite3

# This file can parse the sample csv and add it to a database with defined names.
# It runs the database in memory, there is no permanent storage.
# IT WILL NOT WORK WITH JUST ANY CSV.

# The output is pulled from the created database, not the sample file

# Most of this was created by following and modifying the tutorial at:
# https://www.pythoncentral.io/introduction-to-sqlite-in-python/

# take the data from the csv and put it in an array
sample_file = open("sample_data_2017.csv", "r")
file_contents_by_row = []
for x in range(4,1235): # 1235 is the number of rows in the file
    row = sample_file.readline().split(",")
    file_contents_by_row.append(row)

# create a database file in memory
db = sqlite3.connect(':memory:')

# create a new table in the database

cursor = db.cursor()
cursor.execute('''CREATE TABLE schedules(crn INT PRIMARY KEY, course_id TEXT, component_id TEXT, start_date TEXT, 
    end_date TEXT, day TEXT, start_time TEXT, duration TEXT, pattern_day TEXT, pattern_start_time TEXT, 
    pattern_duration TEXT, building_id TEXT, room_number TEXT, professor TEXT)''')
db.commit()

# this emulates the crn.  There are more steps that need to be done to properly use this.  Currently every new row has
# a new crn.  Eventually classes of the same course_id and component_id will need to have the same crn.
ctr = 0

# fill the table with the array containing the file info
for x in file_contents_by_row[4:1231]:  # 1231 is the number of rows that got parsed into the array
    cursor.execute('''INSERT INTO schedules(crn, course_id, component_id, start_date, end_date, day, start_time, duration,
        pattern_day, pattern_start_time, pattern_duration, building_id, room_number, professor) VALUES(?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?)''', (ctr, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12]))
    ctr += 1
db.commit()

# test
# grab elements and print them to the terminal
cursor.execute('''SELECT course_id, component_id, professor FROM schedules''')
schedule1 = cursor.fetchone()
print(schedule1[0])  # prints the first object that was requested from the database
all_rows = cursor.fetchall()
for row in all_rows:
    print('{0} - {1} : {2}'.format(row[0], row[1], row[2]))  # prints all of the requested objects from the database

db.close()