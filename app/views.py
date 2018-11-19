import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, make_response, session
from werkzeug.utils import secure_filename

from . import auth
from . import database as db

views = Blueprint('views', __name__, template_folder='templates')


@views.route('/skema', methods=['GET'])
def main_page():
    if not session.keys().__contains__('semester') or session['semester'][0] is None or session['semester'][1] > 1:
        return redirect(url_for('views.start'))
    print(session['semester'])
    session['semester'] = session['semester'][0], session['semester'][1] + 1
    subjects = db.get_subject(session['semester'][0])
    profs = db.get_profs(session['semester'][0])
    return render_template('skema.html', subjects=subjects, profs=profs)


@views.route('/skema/data', methods=['GET'])
def return_data():
    print(session)
    request_args = request.args
    years = []
    if 'level100' in request_args:
        years.append(1)
    if 'level200' in request_args:
        years.append(2)
    if 'level300' in request_args:
        years.append(3)
    if 'level400' in request_args:
        years.append(4)
    if 'levelOther' in request_args:
        years.append(5)
        years.append(6)
        years.append(7)
    return db.get_classes(session['semester'][0], request_args['subject'], request_args['prof'], years)


@views.route('/skema/admin', methods=['GET', 'POST'])
@auth.login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file:
            semester = request.form.get("semester") + request.form.get("year")
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            print(semester)
            db.fill_db(semester=semester, file='uploads/' + filename)
            flash('Upload Successful!')
            return redirect(url_for('views.upload', filename=filename))
    return render_template('upload.html')


@views.route('/skema/start', methods=['GET','POST'])
def start():
    if request.method == 'POST':
        toople = request.form.get('semester'), 0
        session['semester'] = toople
        print(session['semester'])
        resp = make_response(redirect(url_for('views.main_page')))
        return resp
    semesters = db.get_semesters()
    return render_template('landing.html', semesters=semesters)

