import datetime
import os
'''
This file manipulates the log file found in the instance folder.
The log file is used to track database manipulation and errors that happen
behind the scenes.
'''


# adds an event to the log in the form:
#
# datetime
# event
def add_event(event):
    log = open('instance/log.txt', 'a+')
    log.write(str(datetime.datetime.now()) + '\n')
    log.write(str(event) + '\n\n')
    log.close()


# deletes the log file.
def rem_log():
    os.remove('instance/log.txt')