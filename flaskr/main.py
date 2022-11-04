from flaskr import create_app, db
from flask import Blueprint, render_template
from models import *


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('base.html')
