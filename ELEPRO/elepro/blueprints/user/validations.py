import re
from wtforms.validators import ValidationError
from elepro.blueprints.user.models import User
from flask_login import current_user


# Niecenzuralne slowa.
forbidden_words = [
    'dupa',
]


def validate_username(form, field):
    """
    Kontrola nazwy uzytkownika.

    :param form: Instancja wtform.
    :param field: Nazwa uzytkownika.
    :return: None
    """
    # Sprawdzenie czy uzytkownik wybral unikalny nick.
    user = User.query.filter_by(username=field.data).first()
    if user:
        raise ValidationError('Ta nazwa użytkownika jest już wykorzystana. Proszę, wybierz inną.')
    # Sprawdzenie czy uzytkownik nie używa niecenzuralnych slow.
    for word in forbidden_words:
        if word in field.data:
            raise ValidationError('Używasz nieodpowiednich słów. Przestrzegaj regulaminu!')


def validate_email(form, field):
    """
    Kontrola maila uzytkownika.

    :param form: Instancja wtform.
    :param field: Mail uzytkownika.
    :return: None
    """
    # Sprawdzenie czy uzytkownik wybral unikalny aders email.
    user = User.query.filter_by(email=field.data).first()
    if user:
        raise ValidationError('Ten adres email jest już wykorzystany. Proszę, wybierz inny.')


def validate_password(form, field):
    """
    Kontrola hasla.

    :param form: Instancja wtform.
    :param field: Hasło uzytkownika.
    :return: None
    """
    # Sprawdzenie czy hasło zawiera przynajmniej jedna litere i cyfre.
    message = 'Hasło musi zawierać przynajmniej jedną literę i cyfrę.'
    input_password = field.data
    if re.search('[0-9]',input_password) is None:
        raise ValidationError(message)
    elif re.search('[a-zA-z]',input_password) is None:
        raise ValidationError(message)


def validate_user_email(form, field):
    """
    Kontrola czy istnieje uzytkownik o podanym adresie email.

    :param form: Instancja wtform.
    :param field: Mail uzytkownika.
    :return: None
    """
    # Sprawdzenie czy uzytkownik wybral unikalny aders email.
    user = User.query.filter_by(email=field.data).first()
    if not user:
        raise ValidationError('Nie ma takiego adresu w naszej bazie danych.')


def validate_update_username(form, field):
    """
    Kontrola nazwy uzytkownika.

    :param form: Instancja wtform.
    :param field: Nazwa uzytkownika.
    :return: None
    """
    # Jesli dane zostały zmienione to sprawdz czy nowa nazwa jest dostepna.
    if field.data != current_user.username:
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Ta nazwa użytkownika jest już wykorzystana. Wybierz inną.')


def validate_update_email(form, field):
    """
    Kontrola nazwy uzytkownika.

    :param form: Instancja wtform.
    :param field: Mail uzytkownika.
    :return: None
    """
    # Jesli dane zostały zmienione to sprawdz czy nowy mail jest dostepny.
    if field.data != current_user.email:
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Ten adres email jest już wykorzystany. Wybierz inną.')
