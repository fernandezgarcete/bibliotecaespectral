# -*- coding: utf-8 -*-

import os
from flask import Flask, current_app, session
from flask_babel import Babel, gettext
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from flask_oidc import OpenIDConnect
from flask_mail import Mail
from flask.json import JSONEncoder
from flask_bootstrap import Bootstrap
#from .momentjs import momentjs
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, WHOOSH_BASE

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#app.jinja_env.globals['momentjs'] = momentjs

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = 'Por favor autentíquese para acceder a la página.'
oid = OpenID(app, os.path.join(basedir, 'tmp'))


mail = Mail(app)

babel = Babel(app)

Bootstrap(app)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/biblioespectral.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('BiblioEspectral Iniciando')

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-responder@' + MAIL_SERVER, ADMINS,
                               'Falla en BibliotecaEspectral', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


class CustomJSONEncoder(JSONEncoder):
    ''' Esta clase agrega soporte para traducciones de texto relajadas al JSON encoder de Flask.
    Esto es necesario cuando se muestran mensajes traducidos.'''

    def default(self, obj):
        from speaklater import is_lazy_string

        if is_lazy_string(obj):
            try:
                return unicode(obj)  # python 2
            except NameError:
                return str(obj)  # python3
        return super(CustomJSONEncoder, self).default(obj)


with app.app_context():
    from app import views, models
