from flask import Flask

from elepro.blueprints.user import user
from elepro.blueprints.post import post
from elepro.blueprints.errors import error


from elepro.extensions import (
    extensions,
    db,
    bcrypt,
    login_manager)

from elepro.config import Config


def create_app(config_class=Config):
    """
    Tworzymy aplikacje flask.

    :param config_class: Klasa ze stalymi do konfiguracji.
    :return: Flask app
    """
    # Instancja aplikacji.
    app = Flask(__name__)
    # Konfiguracja aplikacji.
    app.config.from_object(Config)

    # Rejestracja blueprintow.
    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(error)

    # Dodanie rozszerzen.
    extensions(app)

    return app
