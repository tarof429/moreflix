from flask import Blueprint, render_template
from flask_login import login_required
from moreflix import models

movies_bp = Blueprint('movies_bp', __name__,
    static_folder='static',
    template_folder='templates')

@movies_bp.route('/')
@login_required
def index():
    movies = models.get_all_movies()

    return render_template('index.html', movies=movies)
