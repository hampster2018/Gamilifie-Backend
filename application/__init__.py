from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_session import Session

mongo = PyMongo(tls=True, tlsAllowInvalidCertificates=True)
login_manager = LoginManager()
sesh = Session()

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.secret_key=app.config['SECRET_KEY']

    mongo.init_app(app) 

    login_manager.init_app(app)
    sesh.init_app(app)

    with app.app_context():

        from . import routes
        from . import auth

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        return app