from elepro.extensions import db, login_manager
from flask import current_app, request
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os, secrets, hashlib
import urllib.request


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Model Urzytkownika.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='default.png')
    image_file = db.Column(db.String(60), nullable=False, default='')
    md5_hash = db.Column(db.String(60), nullable=False, default='')
    password = db.Column(db.String(100), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    problems = db.relationship('Problem', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __init__(self, **kwargs):
        """
        Metoda inicjująca i generująca gravatar.
        """
        super(User, self).__init__(**kwargs)
        if self.image_file is None:
            # Adres URL gravataru.
            url = self.gravatar()
            # Utworzenie unikalnej nazwy gravataru.
            random_hex = secrets.token_hex(16)
            picture_fn = random_hex + '.jpg'
            picture_path= os.path.join(current_app.root_path, 'static/images/pictures_of_users', picture_fn)
            # Zapisanie gravataru do folderu z zdjęciami użytkowników.
            urllib.request.urlretrieve(url, picture_path)
            # Aktualizacja pola w tabeli linkie do gravataru.
            self.image_file = picture_fn

    def change_email(self, new_email):
        """
        Metoda zmieniająca maila.

        :param new_email: Nowy adres mail.
        :return: Bool.
        """
        self.email = new_email
        # Musimy zmienić hash md5.
        self.md5_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True


    def gravatar(self, size=125, default='identicon', rating='g'):
        """
        Metoda generujaca adres URL grawataru.

        :param size: Rozmiar gravataru.
        :param default: Typ gravataru.
        :return: URL gravataru.
        """
        if request.is_secure:
            # Dla SSL.
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.md5_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return f'{url}/{hash}?s={size}&d={default}&r={rating}'

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
