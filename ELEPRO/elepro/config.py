# Dane Postgresqla.
POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'elepro',
    'host': '',
    'port': '',
}


class Config():
    """
    Stale konfigurujace aplikacje.
    """

    DEBUG = False
    SECRET_KEY = ''

    # Database.
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:\
                                %(port)s/%(db)s' % POSTGRES

    # Rechapta.
    RECAPTCHA_PUBLIC_KEY = '6LdKt4QUAAAAAC9eaeVlrjl0sE7RaVk5nWjpZzPt'
    RECAPTCHA_PRIVATE_KEY = ''
    RECAPTCHA_PARAMETERS = {'hl': 'pl'}

    # Mail.
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "@gmail.com"
    MAIL_PASSWORD = ""

    FLASKY_POSTS_PER_PAGE = 5
