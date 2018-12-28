from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField)
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


# Kategorie problemu.
categories = [
    ('programowanie', 'programowanie'),
    ('technika analogowa', 'technika analogowa'),
    ('technika cyfrowa', 'technika cyfrowa'),
    ]


# Formularz utworzenia i aktualizacji problemu.
class ProblemForm(FlaskForm):
    title = StringField('Tytuł', validators=[
                                    DataRequired('To pole jest wymagane.'),
                                    Length(min=2, max=300, message='Musisz \
                                    podać przynajmniej 2 znaki.'),])
    category = SelectField('Kategoria', choices=categories,
                            validators=[DataRequired('To pole jest wymagane.')])
    content = TextAreaField('Opis', validators=[
                                            DataRequired('To pole jest wymagane.'),])
    submit = SubmitField('Opublikuj')


# Formularz komentarza.
class CommentForm(FlaskForm):
    body = StringField('Komentarz:', validators=[DataRequired()])
    submit = SubmitField('Skomentuj')
