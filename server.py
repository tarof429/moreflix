from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
import json

dbname='moreflix'
moviesJSON = 'movies.json'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/createdb')
def create_db():
    mongodbUrl = os.environ['MONGODB_URL']

    client = MongoClient(mongodbUrl)

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

@app.route('/findall')
def findall():
    mongodbUrl = os.environ['MONGODB_URL']

    client = MongoClient(mongodbUrl)

    moreflix = client['moreflix']
    movies = moreflix['movies']
    data = list(movies.find({}, {"_id": 0})) # Remove IDs
     
    print(type(data))

    for d in data:
        print(d)

    return jsonify(data)

@app.route('/findbytitle')
def findByTitle():
    title = request.args.get('title')

    mongodbUrl = os.environ['MONGODB_URL']

    client = MongoClient(mongodbUrl)

    moreflix = client['moreflix']
    movies = moreflix['movies']
    query = {"title": {"$regex": title}}
    data = list(movies.find(query, {"_id": 0})) # Remove IDs

    print(type(data))

    for d in data:
        print(d)

    return jsonify(data)

if __name__ == '__main__':
    app.run()