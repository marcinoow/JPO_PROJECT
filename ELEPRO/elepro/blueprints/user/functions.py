from elepro.extensions import mail
from flask_mail import Message
from flask import url_for, current_app
import os, secrets
from PIL import Image


def send_reset_email(user):
    """
    Funkcja wysylajaca maila z linkiem do zresetowania hasla.

    :param user: Uzytkownik do ktorego wysylamy maila.
    :return: None
    """
    # Generowanie tokena.
    token = user.get_reset_token()
    # Utworzenie instancji wiadomosci.
    msg = Message('Resetowanie hasła ElePro', sender='pibermaw@gmail.com',
                                                        recipients=[user.email])
    # Dodanie tresci do instancji wiadomosci.
    msg.body = f"Kliknij poniższy link, aby zresetować hasło:\
                {url_for('user.new_password', token=token, _external=True)}\
                Jeżeli to nie Ty wysłałeś prośbę o zresetowanie hasła, to\
                zignoruj tego maila, a zmiany nie będą wprowadzone.\n\
                Z poważaniem,\n\
                Zespół ElePro"
    # Wyslanie maila.
    mail.send(msg)


def send_confirm_email(user):
    """
    Funkcja wysylajaca maila z prosba o potwierdzenie konta.

    :param user: Uzytkownik do ktorego wysylamy maila.
    :return: None
    """
    # Generowanie tokena.
    token = user.get_reset_token()
    # Utworzenie instancji wiadomosci.
    msg = Message('Potwierdź konto ElePro', sender='pibermaw@gmail.com',
                                                        recipients=[user.email])
    # Dodanie tresci do instancji wiadomosci.
    msg.body = f"Kliknij poniższy link, aby potwierdzić swoje nowe konto:\
                {url_for('user.confirm', token=token, _external=True)}\n\
                Z poważaniem,\n\
                Zespół ElePro"
    # Wyslanie maila.
    mail.send(msg)


def save_picture(form_picture):
    """
    Funkcja zapisujaca zdjecie przeslane przez uzytkownika.

    :param form_picture: Obraz do zapisania.
    :return: Sciezka do pliku.
    """
    # Wygenerowanie losowego tokena.
    hex_name = secrets.token_hex(16)
    # Z przesłanego pliku odczytujemy roszerzenie.
    f_name, f_ext = os.path.splitext(form_picture.filename)
    # Utowrzenie nowej nazwy obrazu.
    picture_fn = hex_name + f_ext
    # Utworzenie ściezki do zapisu.
    picture_path= os.path.join(current_app.root_path, 'static/images/pictures_of_users', picture_fn)
    # Zmiana rozmiaru obrazu.
    output_size = (125,125)
    im = Image.open(form_picture)
    im.thumbnail(output_size)
    # Zapisanie obrazu.
    im.save(picture_path)
    return picture_fn
