import urllib
from pymongo import MongoClient
import os
import json

moviesJSON = 'movies.json'

def get_url():
    username = urllib.parse.quote_plus(os.environ['MONGODB_USER'])
    password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
    server = urllib.parse.quote_plus(os.environ['MONGODB_SERVER'])
    port = urllib.parse.quote_plus(os.environ['MONGODB_PORT'])

    url = 'mongodb://{0}:{1}@{2}:{3}/'.format(username, password, server, port)

    print(url)

    return url

def init_app(app):
    url = get_url()
    
    client = MongoClient(url)
    
    database_name = 'moreflix'
    
    if not database_name in client.list_database_names():
        create_db()

def get_all_movies():
    url = get_url()

    client = MongoClient(url)

    moreflix = client['moreflix']
    movies = moreflix['movies']
    data = list(movies.find({}, {"_id": 0})) # Remove IDs
     
    return data

def create_db():
    url = get_url()

    client = MongoClient(url)

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
    url = get_url()

    client = MongoClient(url)

    moreflix = client['moreflix']
    movies = moreflix['movies']
    query = {"title": {"$regex": title}}
    data = list(movies.find(query, {"_id": 0})) # Remove IDs

    return data