from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


def extensions(app):
    """
    Dodanie do aplikacji rozszerzen.

    :param app: Instancja aplikacji Flask.
    :return: None
    """
    # Inicjalizacja i konfiguracja instancji rozszerzen.
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'


# Utworzenie instancji rozszerzen.
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
