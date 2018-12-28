from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request)

from elepro.extensions import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from elepro.blueprints.user.models import User
from elepro.blueprints.user.functions import (
    send_reset_email,
    send_confirm_email,
    save_picture)

from elepro.blueprints.user.forms import (
    RegistrationForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
    ConfirmForm,
    UpdateAccountForm)


user = Blueprint('user', __name__, template_folder='templates')


# Funkcja widoku logowania.
@user.route('/login', methods=['GET','POST'])
def login():
    # Przekierowanie uzytkownika na storne domowa jesli jest juz zalogowany.
    if current_user.is_authenticated:
        return redirect(url_for('post.home'))
    # Utworzenie formularza logowania.
    form = LoginForm()
    # Sprawdzenie czy formularz jest wypelniony.
    if form.validate_on_submit():
        # Wyszukanie urzytkownika w bazie danych.
        user = User.query.filter_by(email=form.email.data).first()
        # Zalogowanie urzytkownika jesli zostal znaleziony i ma potwierdzone konto.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.confirmed:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f'Zalogowałeś się. Miło Cię widzieć!', 'success')
                return redirect(next_page) if next_page \
                                            else redirect(url_for('post.home'))
            else:
                flash(f'Przed zalogowaniem musisz potwierdzić swoje konto. \
                                                Sprawdź swojego maila.', 'warning')
                return redirect(url_for('user.login'))
        else:
            flash(f'Logowanie nie powiodło się! Sprawdź wprowadzone dane.', 'danger')
    return render_template('user/login.html', form=form)


# Funkcja widoku rejestracji.
@user.route('/register', methods=['GET','POST'])
def register():
    # Przekierowanie uzytkownika na storne domowa jesli jest juz zalogowany.
    if current_user.is_authenticated:
        return redirect(url_for('post.home'))
    # Utworzenie formularza rejestracji.
    form = RegistrationForm()
    # Sprawdzenie czy formularz jest wypelniony.
    if form.validate_on_submit():
        # Hashowanie hasla.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Obiekt urzytkownika do zarejestrowania.
        user = User(username=form.username.data, email=form.email.data,
                                                        password=hashed_password)
        # Dodanie urzytkownika do baz danych.
        db.session.add(user)
        db.session.commit()
        # Wysłanie maila z prośbą potwierdzenia konta.
        send_confirm_email(user)
        flash(f'Twoje konto zostało utworzone. Potwierdź swoją tożsamość za \
            pomocą maila, który zotał wysałny na Twój adres email.', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


# Funkcja potwierdzenia konta.
@user.route('/confirm/<token>')
def confirm(token):
    # Przekierowanie uzytkownika na storne domowa jesli jest juz zalogowany.
    if current_user.is_authenticated:
        return redirect(url_for('post.home'))
    # Sprawdzamy czy token jest aktualny.
    user = User.verify_reset_token(token)
    # Jesli token jest nieaktualny.
    if user is None:
        flash('Wygasł token niezbędny do potwierdzenia konta. Podaj adres email\
         a wyślemy kolejnego maila.', 'danger')
        return redirect(url_for('user.resend_confirmation'))
    else:
        # Jesli token jest aktualny i nie potwierdzono konta.
        if user.confirmed == False:
            user.confirmed = True
            db.session.commit()
            login_user(user)
            flash('Konto zostało potwierdzone. Miło Cię widzieć!', 'success')
        else:
            # Jesli token jest aktualny i potwierdzono konto.
            flash('Konto zostało już potwierdzone.', 'success')
        return redirect(url_for('post.home'))


# Funkcja widoku pobierajaca maila uzytkownika, na ktory zostanie wyslany token.
@user.route('/confirm', methods=['GET', 'POST'])
def resend_confirmation():
    # Przekierowanie uzytkownika na storne domowa jesli jest juz zalogowany.
    if current_user.is_authenticated:
        return redirect(url_for('post.home'))
    # Utworzenie formularza pbierajacego adres email.
    form = ConfirmForm()
    # Jesli formularz jest wypelniony to wysylamy maila z nowym tokenem.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_confirm_email(user)
        flash(f'Mail z linkiem do potwierdzenia konta został wysłany na Twójego maila.', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/unconfirmed.html', form=form)


# Funkcja widoku wylogowania.
@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Wylogowałeś się!', 'success')
    return redirect(url_for('post.home'))


# Funkcja widoku pobierajaca maila uzytkownika, na ktory zostanie wyslany token.
@user.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    # Utworzenie formularza pbierajacego adres email.
    form = RequestResetForm()
    # Jesli formularz jest wypelniony to wysylamy maila z nowym tokenem.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email z instrukcją resetowania hasła został wysłany.', 'info')
        return redirect(url_for('user.reset_password'))
    return render_template('user/reset_password.html', form=form)


# Funkcja widoku resetujaca stare haslo.
@user.route("/reset_password/<token>", methods=['GET', 'POST'])
def new_password(token):
    # Sprawdzenie czy token jest aktualny.
    user = User.verify_reset_token(token)
    if user is None:
        flash('Wygasł token niezbędny do zresetowania hasła. Jeśli chcesz \
        zresetować hasło ponownie prześlij maila.', 'warning')
        return redirect(url_for('post.home'))
    # Utworzenie formularza pbierajacego nowe haslo.
    form = ResetPasswordForm()
    # Jesli formularz jest wypelniony resetujemy haslo.
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Hasło zostało zmienione. Możesz się zalogować.', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/new_password.html', form=form)


# Funkcja widoku profilu użytkownika.
@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Utworzenie formularza do aktualizacji danych.
    form = UpdateAccountForm()
    # Jeśli formularz został przesłany z wypełnionym danymi to zapisz dane.
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.change_email(form.email.data)
        db.session.commit()
        flash(f'Twój profil został zaktualizowany.', 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        # Wypełnienie formularz aktualnymi danymi.
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="images/pictures_of_users/" + current_user.image_file)
    return render_template("user/account.html", form=form, image_file=image_file)
