# -*- coding: utf-8 -*-
__author__ = 'Juanjo'

import os

basedir = os.path.abspath(os.path.dirname(__file__))
sep = os.path.sep
UPLOAD_FOLDER = basedir + sep + 'subidas' + sep
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG'])

DOCUMENTS_FOLDER = basedir+sep+'docs'+sep

### Data Base Configuration ###
db_manager = 'postgresql://'
db_user = 'juanjo'
db_password = 'epsilon1'
db_url = 'localhost'
db_name = 'alchemy'
db_search_whoosh = 'search_alchemy'
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

# API Registro CONAE
TOKEN = 'https://registracionapi.conae.gov.ar/nombrecookie'
DATOS = 'https://registracionapi.conae.gov.ar/datos/'
LOGOUT = 'https://registracionapi.conae.gov.ar/logOut/'
FORMULARIO = 'https://registracionapi.conae.gov.ar/formulario/'
LOGUEO = 'https://registracionapi.conae.gov.ar/logueo/'
# Configuraciones de servidor de mail
MAIL_SERVER = 'mail.conae.gov.ar'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'jjfernandez@conae.gov.ar'
MAIL_PASSWORD = 'Ep$ilon1'

# Lista de administradores
ADMINS = ['jjfernandez@conae.gov.ar']

# pagination
POST_PER_PAGE = 3

# Full text Search
MAX_SEARCH_RESULTS = 50

# available language
LANGUAGES = {
    'en' : 'English',
    'es' : 'Español',
    'pt' : 'Portugues',
    'it' : 'Italiano'
}

#  Microsoft Translation service
MS_TRANSLATOR_CLIENT_ID = 'flask-test-microblog' # ingresar el Id de la app traduccion MS
MS_TRANSLATOR_CLIENT_SECRET = '8IwAJV7BJWEjHcHtvfHOlMv94djxCnIhT3DEKn1jMjQ=' # ingresa tu secreto app traduccion de MS aquí