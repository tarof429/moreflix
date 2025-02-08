
# moreflix example

## Introduction

This containerized web application displays a list of movies stored in MongoDB.

## Build instructions

While developing this application, it can be helpful to only bring up mongo and mongo-express. To do this:

1. Comment out the moreflix service in docker-compose.yml


2. Create the virtual environment.

```sh
python3 -m venv moreflix-venv
```

3. Activate the virtual environment

```sh
. ./moreflix-venv/bin/activate
```

3. Install dependencies

```sh
python3 -m pip install -r requirements.txt
```

4. Run the mongo and mongo-express containers. Hint: see the docker-compose file.

4. Run the application.

```sh
export MONGODB_USER=root
export MONGODB_PASSWORD=secret
export MONGODB_SERVER=localhost
export MONGODB_PORT=27017

flask run --host=0.0.0.0
```

## Running the application (production)

With all 3 services in the docker-compose file:

1. Bring up all the containers

```sh
docker compose up
```

2. Populate the database

```sh
curl http://<ip>:5000/api/v1/createdb
```

3. Point your browser to http://<ip>:5000