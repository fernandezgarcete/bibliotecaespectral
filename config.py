# -*- coding: utf-8 -*-
__author__ = 'Juanjo'

import os

basedir = os.path.abspath(os.path.dirname(__file__))
sep = os.path.sep
UPLOAD_FOLDER = basedir + sep + 'subidas' + sep
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

DOCUMENTS_FOLDER = basedir+sep+'docs'+sep+'documentos'+sep
FICHAS_FOLDER = basedir+sep+'docs'+sep+'fichas'+sep
PROTOCOLOS_FOLDER = basedir+sep+'docs'+sep+'protocolos'+sep
CAMPAIGNS_FOLDER = basedir+sep+'campanias'+sep

### Data Base Configuration ###
db_manager = 'postgresql://'
db_user = 'jjfernandez'
db_password = 'epsilon1'
db_url = 'localhost'
db_name = 'alchemy'
db_search_whoosh = 'search_alchemy'
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5
WHOOSH_BASE = db_manager+db_user+':'+db_password+'@'+db_url+'/'+db_search_whoosh
SQLALCHEMY_DATABASE_URI = db_manager + db_user + ':' + db_password + '@' + db_url + '/' +db_name
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLE = True
SECRET_KEY = 'miclave'

### Open ID Config ###
OPENID_PROVIDERS = [
    {'name':'Yahoo', 'url':'https://me.yahoo.com'}
]

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '232060967171713',
        'secret': '282ea6a34493cbffd9f0f5364e989181'
    },
    'twitter': {
        'id': 'mrUnKQcyGsl184zVB0ZBj3n96',
        'secret': 'MmGrYbKLMlVdgaNje0iRnIPjrYhRln2jBJPVV3R3inaZu8YkYM'
    }
}

# API REGISTRO CONAE DESARROLLO
DEVREG = 'https://dev-api.conae.gov.ar/'
DEVTOKEN = 'https://dev-api.conae.gov.ar/nombrecookie/'
DEVDATOS = 'https://dev-api.conae.gov.ar/datos/'
DEVLOGOUT = 'https://dev-api.conae.gov.ar/logOut/'
DEVFORMULARIO = 'https://dev-api.conae.gov.ar/formulario/'
DEVLOGUEO = 'https://dev-api.conae.gov.ar/logueo/'
USUARIO = 'usuario1@conae.gov.ar'
PASSW = '123456'
# API REGISTRO CONAE PRODUCCION
TOKEN = 'https://registracionapi.conae.gov.ar/nombrecookie/'
DATOS = 'https://registracionapi.conae.gov.ar/datos/'
LOGOUT = 'https://registracionapi.conae.gov.ar/logOut/'
FORMULARIO = 'https://registracionapi.conae.gov.ar/formulario/'
LOGUEO = 'https://registracionapi.conae.gov.ar/logueo/'


# Configuraciones de servidor de mail
MAIL_SERVER = 'mail.conae.gov.ar'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'bibliotecaespectral.udae@conae.gov.ar'
MAIL_PASSWORD = 'M1yi924r'

# Lista de administradores
ADMINS = ['jjfernandez@conae.gov.ar', 'ssu.atencionusuarios@conae.gov.ar', 'mr.juanjo@gmail.com']

# pagination
POST_PER_PAGE = 5

# Full text Search
MAX_SEARCH_RESULTS = 50

# available language
LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'pt': 'Portugues',
    'it': 'Italiano'
}

#  Microsoft Translation service
MS_TRANSLATOR_CLIENT_ID = 'flask-test-microblog' # ingresar el Id de la app traduccion MS
MS_TRANSLATOR_CLIENT_SECRET = '8IwAJV7BJWEjHcHtvfHOlMv94djxCnIhT3DEKn1jMjQ=' # ingresa tu secreto app traduccion de MS aquí

# Google NoCaptcha ReCaptcha API Key
SITE_KEY_CAPTCHA = '6LdBqQwUAAAAAPRfUvYwc78kzaV0BUnHwhyD3zKU'
SECRET_KEY_CAPTCHA = '6LdBqQwUAAAAABVBhVfZPtN0oYef-hl_7jztwheg'