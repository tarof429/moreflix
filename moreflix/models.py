from flask_login import UserMixin
from pymongo import MongoClient
import urllib
import json
import os

moviesJSON = 'movies.json'
database_name = 'moreflix'
collection_name = 'movies'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = { "admin": User(1, "admin", "password" )}

def get_user(username):
    return users.get(username)

def get_client():
    username = urllib.parse.quote_plus(os.environ['MONGODB_USER'])
    password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
    server = urllib.parse.quote_plus(os.environ['MONGODB_SERVER'])
    port = urllib.parse.quote_plus(os.environ['MONGODB_PORT'])

    url = 'mongodb://{0}:{1}@{2}:{3}/'.format(username, password, server, port)

    client = MongoClient(url)

    return client

def init_app(app):
    app.teardown_appcontext(close_client)

def drop_db():
    client = get_client()

    databaseNames = ''

    moreflix = client[database_name]
    movies = moreflix[collection_name]

    movies.drop()

    return []

def create_db():
    client = get_client()

    databaseNames = ''

    try:
        moreflix = client[database_name]
        movies = moreflix[collection_name]

        with open(moviesJSON, 'r') as f:
            data = json.load(f)

        movies.insert_many(data['movies'])

        databaseNames = client.list_database_names()

    except Exception as e:
        print(e)
    return databaseNames

def get_all_movies():
    client = get_client()

    moreflix = client[database_name]
    movies = moreflix[collection_name]
    data = list(movies.find({}, {"_id": 0})) # Remove IDs
     
    return data

def close_client(e=None):
    client = get_client()
    client.close()