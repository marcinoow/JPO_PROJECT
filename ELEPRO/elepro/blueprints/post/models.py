from elepro.extensions import db
from datetime import datetime
from elepro.blueprints.post.forms import categories
from elepro.blueprints.user.models import User


# Model Problemu.
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    state = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='problem', lazy='dynamic')

    @staticmethod
    def generate_fake(count=10):
        """
        Funkcja generujaca przykladowe problemy.
        Wykorzystywana w srodowisku deweloperskim.

        :param count: Liczba falszywych wpisow (problemow).
        :return: None
        """
        from random import seed, randint
        import forgery_py
        seed()
        # liczba uzytkownikow w bazie danych.
        user_count = User.query.count()
        # Liczba kategori problemu.
        category_count = len(categories)
        # Generowanie wpisow.
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            c = categories[randint(0, category_count-1)][0]
            p = Problem(title=forgery_py.lorem_ipsum.title(),
                    category=c,
                    date_posted=forgery_py.date.date(True),
                    content=forgery_py.lorem_ipsum.sentences(randint(5, 15)),
                    author=u)
            # Dodanie wpisu do baz danych.
            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return f"Problem('{self.title}', '{self.date_posted}')"


# Model Komentarza.
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, nullable=False, default=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
