from flask import Flask, jsonify, render_template

from . import db

# Application factory
def create_app():
    app = Flask(__name__)

    # Register the app
    db.init_app(app)

    @app.route('/test')
    def test():
        return "test"

    @app.route('/')
    def index():
        movies = db.get_all_movies()

        return render_template('index.html', movies=movies)

    @app.route('/api/v1/dropdb')
    def drop_all_movies():
       return jsonify(db.drop_db())

    @app.route('/api/v1/createdb')
    def create_db_api():
        return db.create_db()

    @app.route('/api/v1/findall')
    def get_all_movies_api():
        movies = db.get_all_movies()

        return jsonify(movies)

    return app