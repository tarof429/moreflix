from flask import Blueprint, jsonify

from moreflix import models

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/test')
def test():
    return "test"

@api_bp.route('/dropdb')
def drop_all_movies():
    return jsonify(models.drop_db())

@api_bp.route('/createdb')
def create_db_api():
    return models.create_db()

@api_bp.route('/findall')
def get_all_movies_api():
    movies = models.get_all_movies()
    return jsonify(movies)