from . import create_app
from flask import Blueprint, render_template
from . import db


main = Blueprint('main', __name__)

@main.route('/')
def base():
    return render_template('base.html')
