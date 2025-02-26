# Moreflix

## Introduction

This containerized web application displays a list of movies stored in MongoDB.

# Development

While developing this application, it can be helpful to only bring up mongo and mongo-express. To do this:

1. Comment out the moreflix service in docker-compose.yml

2. Start the services using docker compose.

```sh
COMPOSE_PROFILES=db docker compose up -d
```

Next, bring up the application.

1. Create the virtual environment.

```sh
python3 -m venv moreflix-venv
```

2. Activate the virtual environment

```sh
. ./moreflix-venv/bin/activate
```

3. Install dependencies. This needs to be done only once, or if dependencies change.

```sh
python3 -m pip install -r requirements.txt
```

4. Start the application.

```sh
. ./moreflix-venv/bin/activate
export MONGODB_USER=root
export MONGODB_PASSWORD=secret
export MONGODB_SERVER=localhost
export MONGODB_PORT=27017
flask --app moreflix run --debug
```

5. To bring down the services

```sh
COMPOSE_PROFILES=db docker compose down
```

6. Type Ctrl-X in the window running moreflix to shut it down.

## Running the application (production)

In this environment, moreflix will be brought up as a service. Take care that your shell environment does not override any environment variables defined in the .env file.

1. Start a new terminal window.

2. Build the moreflix image.

```sh
docker build -t tarof429/moreflix:1.0 .
```

3. If the moreflix service was commented out in docker-compose.yml, uncomment it.

4. Bring up all 3 services in the docker-compose file:

```sh
COMPOSE_PROFILES=db,app docker compose up -d
```

## Using the application

1. Point your browser to http://localhost:5000

2. To drop the database

```sh
curl http://localhost:5000/api/v1/dropdb
```

3. To populate the database

```sh
curl http://localhost:5000/api/v1/createdb
```

