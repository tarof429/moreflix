from flask import Blueprint, render_template

from moreflix import models

welcome_bp = Blueprint('welcome_bp', __name__,
    static_folder='static',
    template_folder='templates')

@welcome_bp.route('/')
def index():
    return render_template('welcome.html')
