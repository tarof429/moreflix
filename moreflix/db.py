import urllib
from pymongo import MongoClient
import os
import json

moviesJSON = 'movies.json'

def get_client():
    username = urllib.parse.quote_plus(os.environ['MONGODB_USER'])
    password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
    server = urllib.parse.quote_plus(os.environ['MONGODB_SERVER'])
    port = urllib.parse.quote_plus(os.environ['MONGODB_PORT'])

    url = 'mongodb://{0}:{1}@{2}:{3}/'.format(username, password, server, port)

    client = MongoClient(url)

    return client

def close_client(e=None):
    client = get_client()
    client.close()

def init_db():
    client = get_client()

    database_name = 'moreflix'
    
    if not database_name in client.list_database_names():
        return create_db()

def init_app(app):
    app.teardown_appcontext(close_client)

def get_all_movies():
    client = get_client()

    moreflix = client['moreflix']
    movies = moreflix['movies']
    data = list(movies.find({}, {"_id": 0})) # Remove IDs
     
    return data

def create_db():
    client = get_client()

    databaseNames = ''

    try:
        moreflix = client['moreflix']
        movies = moreflix['movies']

        with open(moviesJSON, 'r') as f:
            data = json.load(f)

        movies.insert_many(data['movies'])

        databaseNames = client.list_database_names()

    except Exception as e:
        print(e)
    return databaseNames

def find_by_title(title):
    client = get_client()

    moreflix = client['moreflix']
    movies = moreflix['movies']
    query = {"title": {"$regex": title}}
    data = list(movies.find(query, {"_id": 0})) # Remove IDs

    return data