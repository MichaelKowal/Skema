from flask import Blueprint, render_template

views = Blueprint('views', __name__, template_folder='templates')

@views.route('/skema', methods=['GET'])
def main_page():
    return render_template('skema.html')


