from flask import Blueprint, render_template, request
from . import database as db
views = Blueprint('views', __name__, template_folder='templates')


@views.route('/skema', methods=['GET'])
def main_page():
    subjects = db.get_subject()
    profs = db.get_profs()
    return render_template('skema.html', subjects=subjects, profs=profs)


@views.route('/data')
def return_data():
    requestArgs = request.args
    years = []
    if 'level100' in requestArgs:
        years.append(1)
    if 'level200' in requestArgs:
        years.append(2)
    if 'level300' in requestArgs:
        years.append(3)
    if 'level400' in requestArgs:
        years.append(4)
    if 'level500' in requestArgs:
        years.append(5)
    return db.get_classes(requestArgs['subject'], requestArgs['prof'], years)

