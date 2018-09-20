from flask import Blueprint, render_template

views = Blueprint('views', __name__, template_folder='templates')

@views.route('/skema', methods=['GET'])
def main_page():
    return render_template('skema.html')


'''
@views.route('/info', methods=['GET'])
def info():
    return render_template('info.html')
'''
