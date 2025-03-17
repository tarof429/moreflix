from flask import Flask
from flask_session import Session
from redis import Redis
import urllib
import os
import secrets

from moreflix.api.api import api_bp
from moreflix.movies.movies import movies_bp
from moreflix.auth.auth import auth_bp
from moreflix.welcome.welcome import welcome_bp
from moreflix.extensions import login_manager
from moreflix.models import init_app, get_user, users

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_bytes(32)
    redis_server = urllib.parse.quote_plus(os.environ['REDIS_SERVER'])
    redis_port = urllib.parse.quote_plus(os.environ['REDIS_PORT'])

    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis.from_url('redis://{0}:{1}'.format(redis_server, redis_port))
    Session(app)
    
    init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(movies_bp, url_prefix='/movies')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(welcome_bp, url_prefix='/')
    
    @login_manager.user_loader
    def load_user(id):
        for user in users.values():
            if user.id == int(id):
                return user
        return None
    
    return app