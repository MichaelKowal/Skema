import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
import flask_uploads
from werkzeug.utils import secure_filename
from . import database as db
from . import auth

views = Blueprint('views', __name__, template_folder='templates')


@views.route('/skema', methods=['GET'])
def main_page():
    subjects = db.get_subject()
    profs = db.get_profs()
    return render_template('skema.html', subjects=subjects, profs=profs)


@views.route('/data')
def return_data():
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
    return db.get_classes(request_args['subject'], request_args['prof'], years)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() is 'csv'


@views.route('/upload', methods=['GET', 'POST'])
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
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            flash('Upload Successful!')
            return redirect(url_for('views.upload', filename=filename))
    return render_template('upload.html')

