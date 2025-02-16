from flask import Flask, jsonify, request, render_template
from . import db 

def create_app():
    app = Flask(__name__)

    db.init_app(app)

    @app.route('/')
    def get_all_movies_ui():
        return render_template('index.html', data=db.get_all_movies())

    @ app.route('/test')
    def test():
        print("Yup, I'm here")
        return "test"

    @app.route('/api/v1/findall')
    def get_all_movies_api():
        return jsonify(db.get_all_movies())
        
    @app.route('/api/v1/findbytitle')
    def find_by_title_api():
        title = request.args.get('title')

        data = db.find_by_title(title)

        return jsonify(data)

    @app.route('/api/v1/createdb')
    def create_db_api():
        return db.create_db()

    return app
