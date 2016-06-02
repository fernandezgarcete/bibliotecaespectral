# -*- coding: utf-8 -*-
from flask import current_app, url_for
from rauth import OAuth2Service, OAuth1Service

__author__ = 'Juanjo'

from hashlib import md5
from app import db, app
from geoalchemy2 import Geometry
from flask_login import UserMixin
import sys, re

if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


''' Tablas del Radiometro '''

# Tabla Localidad
class Localidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(140), index=True, unique=True)
    campanias = db.relationship('Campania', backref='localidad_campania', lazy='dynamic')


# Tabla Proyecto
class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(140))
    descripcion = db.Column(db.String(140))
    integrantes = db.Column(db.String(200))
    responsable = db.Column(db.String(50))
    status = db.Column(db.Boolean)
    campanias = db.relationship('Campania', backref='proyecto_campania', lazy='dynamic')

    @property
    def start(self):
        return self.status(True)

    @property
    def stop(self):
        return self.status(False)

    @property
    def is_active(self):
        if self.status is True:
            return True
        return False


# Tabla Campaña
class Campania(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    fecha = db.Column(db.DateTime)
    responsable = db.Column(db.String(140))
    id_localidad = db.Column(db.Integer, db.ForeignKey('localidad.id'))
    objetivo = db.Column(db.String(140))
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))
    id_muestra = db.Column(db.Integer, db.ForeignKey('unidad_muestral.id'))

    @property
    def is_complete(self):
        return True


# Tabla tipo de cobertura
class TipoCobertura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    coberturas = db.relationship('Cobertura', backref='cobertura', lazy='dynamic')


# Tabla Cobertura
class Cobertura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    id_tipocobertura = db.Column(db.Integer, db.ForeignKey('tipo_cobertura.id'))
    altura = db.Column(db.DECIMAL(precision=2))
    fenologia = db.Column(db.String(140))
    observaciones = db.Column(db.String(140))
    muestras = db.relationship('UnidadMuestral', backref='cobertura_muestra', lazy='dynamic')


# Tabla Unidad Muestral
class UnidadMuestral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    id_metodologia = db.Column(db.Integer, db.ForeignKey('metodologia.id'))
    id_instrumento = db.Column(db.String(80), db.ForeignKey('instrumento.id'))
    operador = db.Column(db.String(80))
    uuid = db.Column(db.String(80))
    id_cobertura = db.Column(db.Integer, db.ForeignKey('cobertura.id'))
    puntos = db.relationship('Punto', backref='punto', lazy='dynamic')

# Tabla Instrumento
class Instrumento(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    tipo = db.Column(db.String(140))
    instrumento = db.Column(db.String(140))
    marca = db.Column(db.String(80))
    modelo = db.Column(db.String(80))
    rango_espectral = db.Column(db.String(80))
    resolucion_espectral = db.Column(db.String(80))
    ancho_banda = db.Column(db.String(80))
    tiempo_escaneo = db.Column(db.DECIMAL(precision=2))
    reproducibilidad_ancho_banda = db.Column(db.DECIMAL(precision=2))
    exactitud_ancho_banda = db.Column(db.DECIMAL(precision=2))
    detector_vnir = db.Column(db.String(80))
    detector_swir1 = db.Column(db.String(80))
    detector_swir2 = db.Column(db.String(80))
    noice_equivalence_radiance_vnir = db.Column(db.String(80))
    noice_equivalence_radiance_swir1 = db.Column(db.String(80))
    noice_equivalence_radiance_swir2 = db.Column(db.String(80))
    largo_fibra_optica = db.Column(db.DECIMAL(precision=2))
    fov = db.Column(db.DECIMAL(precision=3))
    fov_cosenoidal = db.Column(db.String(80))
    muestras = db.relationship('UnidadMuestral', backref='instrumento_muestra', lazy='dynamic')


# Tabla metodologia
class Metodologia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    descripcion = db.Column(db.String(140))
    metodologia_medicion = db.Column(db.String(80))
    angulo_cenital = db.Column(db.DECIMAL(precision=2))
    angulo_azimutal = db.Column(db.DECIMAL(precision=2))
    muestras = db.relationship('UnidadMuestral', backref='metodo_muestra', lazy='dynamic')


# Tabla Punto
class Punto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    fecha_hora = db.Column(db.DateTime)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    altura_medicion = db.Column(db.DECIMAL(precision=2))
    presion = db.Column(db.DECIMAL(precision=2))
    temperatura = db.Column(db.DECIMAL(precision=2))
    nubosidad = db.Column(db.Integer)
    viento_direccion = db.Column(db.String(40))
    viento_velocidad = db.Column(db.DECIMAL(precision=2))
    estado = db.Column(db.String(140))
    cantidad_tomas = db.Column(db.Integer)
    oleaje = db.Column(db.String(80))
    observaciones = db.Column(db.String(240))
    foto = db.Column(db.String(50))
    id_muestra = db.Column(db.Integer, db.ForeignKey('unidad_muestral.id'))
    radiometrias = db.relationship('Radiometria', backref='punto_radiometria', lazy='dynamic')
    fotometrias = db.relationship('Fotometria', backref='Fotometria', lazy='dynamic')
    productos_radiancias = db.relationship('ProductoRadiancia', backref='producto_radiancia_punto', lazy='dynamic')


# Tabla Fotometria
class Fotometria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sig380 = db.Column(db.DECIMAL(precision=7))
    sig500 = db.Column(db.DECIMAL(precision=7))
    sig675 = db.Column(db.DECIMAL(precision=7))
    sig870 = db.Column(db.DECIMAL(precision=7))
    sig1020 = db.Column(db.DECIMAL(precision=7))
    std380 = db.Column(db.DECIMAL(precision=7))
    std500 = db.Column(db.DECIMAL(precision=7))
    std675 = db.Column(db.DECIMAL(precision=7))
    std870 = db.Column(db.DECIMAL(precision=7))
    std1020 = db.Column(db.DECIMAL(precision=7))
    std380 = db.Column(db.DECIMAL(precision=7))
    r380 = db.Column(db.DECIMAL(precision=7))
    r500 = db.Column(db.DECIMAL(precision=7))
    r675 = db.Column(db.DECIMAL(precision=7))
    r870 = db.Column(db.DECIMAL(precision=7))
    r1020 = db.Column(db.DECIMAL(precision=7))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))


# Tabla Producto Radiancia
class ProductoRadiancia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reflectancia = db.Column(db.DECIMAL(precision=20))
    radiancia_avg = db.Column(db.DECIMAL(precision=20))
    radiancia_std = db.Column(db.DECIMAL(precision=20))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))


# Tabla Radiometria
class Radiometria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer, unique=True)
    radiancia = db.Column(db.DECIMAL(precision=20))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    id_superficie = db.Column(db.Integer, db.ForeignKey('superficie.id'))


# Tabla Superficie
class Superficie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    radiometrias = db.relationship('Radiometria', backref='superficie_radiometria', lazy='dynamic')
''' ------- '''


# Creamos la tabla "seguidores" para asociación muchos-a-muchos y autorreferenciada en usuario
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# Entidad Usuario con sus respectivos métodos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def avatar(self, size):

        if self.email is None:
            self.email = 'example@miweb.com'
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def get_id(self):
        try:
            return unicode(self.id) # python 2
        except NameError:
            return str(self.id)

    def __repr__(self): # pragma: no cover
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post %r>' % (self.body)


if enable_search:
    whooshalchemy.whoosh_index(app, Post)

