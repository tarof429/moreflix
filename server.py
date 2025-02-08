from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os
import json
import urllib

moviesJSON = 'movies.json'

app = Flask(__name__)

def get_url():
    username = urllib.parse.quote_plus(os.environ['MONGODB_USER'])
    password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
    server = urllib.parse.quote_plus(os.environ['MONGODB_SERVER'])
    port = urllib.parse.quote_plus(os.environ['MONGODB_PORT'])

    url = 'mongodb://{0}:{1}@{2}:{3}/'.format(username, password, server, port)

    print(url)

    return url

def get_all_movies():
    url = get_url()

    client = MongoClient(url)

    moreflix = client['moreflix']
    movies = moreflix['movies']
    data = list(movies.find({}, {"_id": 0})) # Remove IDs
     
    return data

@app.route('/')
def get_all_movies_ui():
    return render_template('index.html', data=get_all_movies())

@ app.route('/test')
def test():
    print("Yup, I'm here")
    return "test"

@app.route('/api/v1/findall')
def get_all_movies_api():
    return jsonify(get_all_movies())

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

@app.route('/api/v1/createdb')
def create_db_api():
    return create_db()

def find_by_title(title):
    url = get_url()

    client = MongoClient(url)

    moreflix = client['moreflix']
    movies = moreflix['movies']
    query = {"title": {"$regex": title}}
    data = list(movies.find(query, {"_id": 0})) # Remove IDs

    return data

@app.route('/api/v1/findbytitle')
def find_by_title_api():
    title = request.args.get('title')

    data = find_by_title(title)

    return jsonify(data)

if __name__ == '__main__':
    app.run()