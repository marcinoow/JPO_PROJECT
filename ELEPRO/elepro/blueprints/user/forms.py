from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from elepro.blueprints.user.validations import (
    validate_username,
    validate_email,
    validate_password,
    validate_user_email,
    validate_update_username,
    validate_update_email)


# Formularz rejestracji.
class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[
                                                    DataRequired('To pole jest wymagane.'),
                                                    Length(min=2, max=20, message='Musisz \
                                                    podać od 6 do 20 znaków.'),
                                                    validate_username])
    email = StringField('Email', validators=[DataRequired('To pole jest wymagane.'),
                                             Email(message='Wprowadź tutaj adres email.'),
                                             validate_email])
    password = PasswordField('Hasło', validators=[
                                            DataRequired('To pole jest wymagane.'),
                                            Length(min=6, max=20, message='Musisz podać \
                                            od 6 do 20 znaków.'),
                                            validate_password])
    confirm_password = PasswordField('Potwierdź hasło', validators=[
                                                            DataRequired('To pole jest wymagane.'),
                                                            EqualTo('password', message='Hasła \
                                                            muszą być takie same.')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Zarejestruj mnie')


# Formularz logowania.
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('To pole jest wymagane.'), Email()])
    password = PasswordField('Hasło', validators=[DataRequired('To pole jest wymagane.')])
    remember = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Zaloguj mnie')


# Formularz resetowania hasla.
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), validate_user_email])
    recaptcha = RecaptchaField()
    submit = SubmitField('Wyślij maila')


# Formularz wprowadzania nowego hasla.
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[
                                                            DataRequired(),
                                                            EqualTo('password'),
                                                            validate_password])
    submit = SubmitField('Resetuj hasło')


# Formularz pobrania maila do potwierdzenie konta.
class ConfirmForm(FlaskForm):
    email = StringField('Email', validators=[
                                        DataRequired(),
                                        Email(),
                                        validate_user_email])
    recaptcha = RecaptchaField()
    submit = SubmitField('Wyślij maila')


# Formularz aktualizacji danych uzytkownika.
class UpdateAccountForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[
                                                    DataRequired(),
                                                    Length(min=2, max=20),
                                                    validate_update_username])
    email = StringField('Email', validators=[DataRequired(), Email(),
                                                        validate_update_email])
    picture = FileField('Zaktualizuj zdjęcie profilowe', validators=[
                                                            FileAllowed(['jpg','png'])])
    submit = SubmitField('Zmień')
