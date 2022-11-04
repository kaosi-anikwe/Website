from flaskr import create_app, db
from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user
from flaskr.models import *


main = Blueprint('main', __name__)

@main.route('/')
def base():
    return render_template('base.html')
