from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

from . import db

# moreflix application factory
def create_app():
    app = Flask(__name__)

    db.init_app(app)
    #db.init_db() # optional; we could do this step manually

    @app.route('/')
    def index():
        movies = db.get_all_movies()

        return render_template('index.html', movies=movies)

    @ app.route('/test')
    def test():
        print("Yup, I'm here")
        return "test"

    @app.route('/api/v1/findall')
    def get_all_movies_api():
        movies = db.get_all_movies()

        return jsonify(movies)
        
    @app.route('/api/v1/findbytitle')
    def find_by_title_api():
        title = request.args.get('title')

        movies = db.find_by_title(title)

        return jsonify(movies)

    @app.route('/api/v1/createdb')
    def create_db_api():
        return db.create_db()

    return app
