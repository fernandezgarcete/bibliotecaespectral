# -*- coding: utf-8 -*-
from datetime import datetime
import os
import traceback
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
    nombre = db.Column(db.String(140), index=True)
    nombre_dpto = db.Column(db.String(140))
    nombre_prov = db.Column(db.String(140))
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    campanias = db.relationship('Campania', backref='localidad_campania', lazy='dynamic',
                                cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_campania(self, campania):
        return self.campanias.filter(campania.id_localidad == self.id).count() > 0

    def add_campania(self, campania):
        if not self.has_campania(campania):
            self.campanias.append(campania)
            return self

    def get_campanias(self):
        return Campania.query.filter(Campania.id_localidad == self.id).order_by(Campania.fecha.desc()).all()

    def __repr__(self): # pragma: no cover
        return '<Localidad %r>' % (self.nombre)

    def agregar(self, lat, lng, nombre):
        res = db.engine.execute("SELECT b.nombre, b.nom_depto, b.nom_prov, b.the_geom FROM bahra.base b "
                                "WHERE b.nombre LIKE (%s) AND (b.tipo LIKE 'LOCALIDAD' OR b.ubicacion LIKE 'PULOC') "
                                "ORDER BY b.the_geom <-> ST_SetSRID(ST_MakePoint("+lat+","+lng+"),4326) LIMIT 1;", (nombre,)).fetchone()
        if res is not None:
            loc = self.query.filter_by(geom=res[3]).first()
            if loc is None:
                self.nombre = res[0]
                self.nombre_dpto = res[1]
                self.nombre_prov = res[2]
                self.geom = res[3]
                db.session.add(self)
                db.session.commit()
                return True
            elif loc is not None:
                return 'Ya existe'
            else:
                return False
        else:
            return False

# Tabla Proyecto
class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(140), nullable=False, unique=True)
    descripcion = db.Column(db.String(600))
    responsables = db.Column(db.String(340))
    status = db.Column(db.Boolean)
    campanias = db.relationship('Campania', backref='proyecto_campania', lazy='dynamic',
                                cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

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

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_campania(self, campania):
        return self.campanias.filter(campania.id_proyecto == self.id).count() > 0

    def add_campania(self, campania):
        if not self.has_campania(campania):
            self.campanias.append(campania)
            return self

    def get_campanias(self):
        return Campania.query.filter(Campania.id_proyecto == self.id).order_by(Campania.fecha.desc()).all()

    def agregar(self, form):
        proyecto = self
        if int(form.id.data) > 0:
            proyecto = self.query.filter_by(id=int(form.id.data)).first()
            proyecto.nombre = form.nombre.data
            proyecto.descripcion = str(form.descripcion.data).replace('\r\n', ' ')
            proyecto.responsables = form.responsables.data
            proyecto.status = bool(form.status.data)
        else:
            proyecto.nombre = form.nombre.data
            proyecto.descripcion = str(form.descripcion.data).replace('\r\n', ' ')
            proyecto.responsables = form.responsables.data
            proyecto.status = bool(form.status.data)
        try:
            db.session.add(proyecto)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    def __repr__(self): # pragma: no cover
        return '<Proyecto %r>' % (self.nombre)

# Tabla Campaña
class Campania(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    fecha = db.Column(db.DateTime)
    fecha_publicacion = db.Column(db.DateTime)
    responsables = db.Column(db.String(340))
    id_localidad = db.Column(db.Integer, db.ForeignKey('localidad.id'))
    objetivo = db.Column(db.String(140))
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))
    muestras = db.relationship('Muestra', backref='campania_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_campania == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_campania == self.id).all()

    @property
    def is_complete(self):
        return True

    def __repr__(self): # pragma: no cover
        return '<Campaña %r>' % (self.nombre)

# Tabla tipo de cobertura
class TipoCobertura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    coberturas = db.relationship('Cobertura', backref='cobertura', lazy='dynamic',
                                 cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_cobertura(self, cobertura):
        return self.coberturas.filter(cobertura.id_tipocobertura == self.id).count() > 0

    def add_cobertura(self, cobertura):
        if not self.has_cobertura(cobertura):
            self.coberturas.append(cobertura)
            return self

    def get_coberturas(self):
        return Cobertura.query.filter(Cobertura.id_tipocobertura == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Tipo de Cobertura %r>' % (self.nombre)

# Tabla Cobertura
class Cobertura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    id_tipocobertura = db.Column(db.Integer, db.ForeignKey('tipo_cobertura.id'))
    altura = db.Column(db.DECIMAL(precision=5, scale=2))
    fenologia = db.Column(db.String(140))
    observaciones = db.Column(db.String(140))
    muestras = db.relationship('Muestra', backref='cobertura_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_cobertura == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_cobertura == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Cobertura %r>' % (self.nombre)

# Tabla Muestra
class Muestra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    operador = db.Column(db.String(80))
    uuid = db.Column(db.String(80))
    id_cobertura = db.Column(db.Integer, db.ForeignKey('cobertura.id'))
    id_campania = db.Column(db.Integer, db.ForeignKey('campania.id'))
    id_metodologia = db.Column(db.Integer, db.ForeignKey('metodologia.id'))
    id_radiometro = db.Column(db.Integer, db.ForeignKey('radiometro.id'))
    id_camara = db.Column(db.Integer, db.ForeignKey('camara.id'))
    id_gps = db.Column(db.Integer, db.ForeignKey('gps.id'))
    id_fotometro = db.Column(db.Integer, db.ForeignKey('fotometro.id'))
    id_patron = db.Column(db.Integer, db.ForeignKey('patron.id'))
    puntos = db.relationship('Punto', backref='punto', lazy='dynamic',
                             cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_punto(self, punto):
        return self.coberturas.filter(punto.id_muestra == self.id).count() > 0

    def add_punto(self, punto):
        if not self.has_punto(punto):
            self.puntos.append(punto)
            return self

    def get_puntos(self):
        return Punto.query.filter(Punto.id_muestra == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Muestra %r>' % (self.nombre)

# Tabla Camara
class Camara(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80))
    nombre = db.Column(db.String(140), nullable=False, unique=True)
    marca = db.Column(db.String(80))
    modelo = db.Column(db.String(80))
    nro_serie = db.Column(db.String(40))
    accesorio = db.Column(db.String(340))
    muestras = db.relationship('Muestra', backref='camara_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_camara == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_camara == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Cámara %r>' % (self.nombre)

# Tabla GPS
class Gps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80))
    nombre = db.Column(db.String(140), nullable=False, unique=True)
    marca = db.Column(db.String(80))
    modelo = db.Column(db.String(80))
    nro_serie = db.Column(db.String(40))
    accesorio = db.Column(db.String(340))
    muestras = db.relationship('Muestra', backref='gps_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_gps == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_gps == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<GPS %r>' % (self.nombre)

# Tabla Fotometro
class Fotometro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80))
    nombre = db.Column(db.String(140), nullable=False, unique=True)
    marca = db.Column(db.String(80))
    modelo = db.Column(db.String(80))
    nro_serie = db.Column(db.String(40))
    accesorio = db.Column(db.String(340))
    muestras = db.relationship('Muestra', backref='fotometro_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_fotometro == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_fotometro == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<GPS %r>' % (self.nombre)

# Tabla Patron
class Patron(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80))
    nombre = db.Column(db.String(140), nullable=False, unique=True)
    marca = db.Column(db.String(80))
    modelo = db.Column(db.String(80))
    nro_serie = db.Column(db.String(40))
    accesorio = db.Column(db.String(340))
    muestras = db.relationship('Muestra', backref='patron_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_patron == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_patron == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Patron %r>' % (self.nombre)

# Tabla Radiometro
class Radiometro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80))
    nombre = db.Column(db.String(140), nullable=False, unique=True)
    marca = db.Column(db.String(80))
    modelo = db.Column(db.String(80))
    nro_serie = db.Column(db.String(40))
    rango_espectral = db.Column(db.String(80))
    resolucion_espectral = db.Column(db.String(80))
    ancho_banda = db.Column(db.String(80))
    tiempo_escaneo = db.Column(db.DECIMAL(precision=5, scale=2))
    reproducibilidad_ancho_banda = db.Column(db.DECIMAL(precision=5, scale=2))
    exactitud_ancho_banda = db.Column(db.DECIMAL(precision=5, scale=2))
    detector_vnir = db.Column(db.String(120))
    detector_swir1 = db.Column(db.String(120))
    detector_swir2 = db.Column(db.String(120))
    noice_equivalence_radiance_vnir = db.Column(db.String(120))
    noice_equivalence_radiance_swir1 = db.Column(db.String(120))
    noice_equivalence_radiance_swir2 = db.Column(db.String(120))
    largo_fibra_optica = db.Column(db.DECIMAL(precision=5, scale=2))
    fov = db.Column(db.DECIMAL(precision=5, scale=2))
    fov_cosenoidal = db.Column(db.String(80))
    accesorio = db.Column(db.String(340))
    muestras = db.relationship('Muestra', backref='radiometro_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_radiometro == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_radiometro == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Espectrorradiómetro %r>' % (self.nombre)

# Tabla Metodologia
class Metodologia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(600))
    metodologia_medicion = db.Column(db.String(600))
    angulo_cenital = db.Column(db.DECIMAL(precision=5, scale=2))
    angulo_azimutal = db.Column(db.DECIMAL(precision=5, scale=2))
    muestras = db.relationship('Muestra', backref='metodo_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_metodologia == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_metodologia == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Metodología %r>' % (self.nombre)

    def agregar(self, form):
        metod = self
        if int(form.id.data) > 0:
            metod = self.query.filter_by(id=int(form.id.data)).first()
            metod.nombre = form.nombre.data
            metod.descripcion = str(form.descripcion.data).replace('\r\n', ' ')
            metod.metodologia_medicion = str(form.medicion.data).replace('\r\n', ' ')
            metod.angulo_cenital = int(form.cenit.data)
            metod.angulo_azimutal = int(form.azimut.data)
        else:
            metod.nombre = form.nombre.data
            metod.descripcion = str(form.descripcion.data).replace('\r\n', ' ')
            metod.metodologia_medicion = str(form.medicion.data).replace('\r\n', ' ')
            metod.angulo_cenital = int(form.cenit.data)
            metod.angulo_azimutal = int(form.azimut.data)
        try:
            db.session.add(metod)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

# Tabla Punto
class Punto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    fecha_hora = db.Column(db.DateTime)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    altura_medicion = db.Column(db.DECIMAL(precision=6, scale=3))
    presion = db.Column(db.DECIMAL(precision=6, scale=2))
    temperatura = db.Column(db.DECIMAL(precision=5, scale=2))
    nubosidad = db.Column(db.Integer)
    viento_direccion = db.Column(db.String(40))
    viento_velocidad = db.Column(db.DECIMAL(precision=5, scale=2))
    estado = db.Column(db.String(140))
    cantidad_tomas = db.Column(db.Integer)
    oleaje = db.Column(db.String(80))
    observaciones = db.Column(db.String(240))
    foto = db.Column(db.String(50))
    id_muestra = db.Column(db.Integer, db.ForeignKey('muestra.id'))
    radiometrias = db.relationship('Radiometria', backref='punto_radiometria', lazy='dynamic',
                                   cascade="save-update, merge, delete")
    fotometrias = db.relationship('Fotometria', backref='Fotometria', lazy='dynamic',
                                  cascade="save-update, merge, delete")
    productos_radiancias = db.relationship('ProductoRadiancia', backref='producto_radiancia_punto', lazy='dynamic',
                                           cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_radiometria(self, radiometria):
        return self.radiometrias.filter(radiometria.id_punto == self.id).count() > 0

    def add_radiometria(self, radiometria):
        if not self.has_radiometria(radiometria):
            self.radiometrias.append(radiometria)
            return self

    def get_radiometrias(self):
        return Radiometria.query.filter(Radiometria.id_punto == self.id).all()

    def has_fotometria(self, fotometria):
        return self.fotometrias.filter(fotometria.id_punto == self.id).count() > 0

    def add_fotometria(self, fotometria):
        if not self.has_fotometria(fotometria):
            self.fotometrias.append(fotometria)
            return self

    def get_fotometrias(self):
        return Fotometria.query.filter(Fotometria.id_punto == self.id).all()

    def has_producto_radiancia(self, producto_radiancia):
        return self.productos_radiancias.filter(producto_radiancia.id_punto == self.id).count() > 0

    def add_producto_radiancia(self, producto_radiancia):
        if not self.has_producto_radiancia(producto_radiancia):
            self.productos_radiancias.append(producto_radiancia)
            return self

    def get_productos_radiancias(self):
        return ProductoRadiancia.query.filter(ProductoRadiancia.id_punto == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Punto %r>' % (self.nombre)

# Tabla Fotometria
class Fotometria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sig380 = db.Column(db.DECIMAL(precision=12, scale=7))
    sig500 = db.Column(db.DECIMAL(precision=12, scale=7))
    sig675 = db.Column(db.DECIMAL(precision=12, scale=7))
    sig870 = db.Column(db.DECIMAL(precision=12, scale=7))
    sig1020 = db.Column(db.DECIMAL(precision=12, scale=7))
    std380 = db.Column(db.DECIMAL(precision=12, scale=7))
    std500 = db.Column(db.DECIMAL(precision=12, scale=7))
    std675 = db.Column(db.DECIMAL(precision=12, scale=7))
    std870 = db.Column(db.DECIMAL(precision=12, scale=7))
    std1020 = db.Column(db.DECIMAL(precision=12, scale=7))
    r380 = db.Column(db.DECIMAL(precision=12, scale=7))
    r500 = db.Column(db.DECIMAL(precision=12, scale=7))
    r675 = db.Column(db.DECIMAL(precision=12, scale=7))
    r870 = db.Column(db.DECIMAL(precision=12, scale=7))
    r1020 = db.Column(db.DECIMAL(precision=12, scale=7))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self): # pragma: no cover
        return '<Fotometria %r>' % (str(self.id))

# Tabla Producto Radiancia
class ProductoRadiancia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    reflectancia = db.Column(db.DECIMAL(precision=20, scale=15))
    radiancia_avg = db.Column(db.DECIMAL(precision=20, scale=15))
    radiancia_std = db.Column(db.DECIMAL(precision=20, scale=15))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self): # pragma: no cover
        return '<Producto Radiancia %r>' % (str(self.id))

# Tabla Radiometria
class Radiometria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    radiancia = db.Column(db.DECIMAL(precision=20, scale=15))
    toma = db.Column(db.Integer)
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    id_superficie = db.Column(db.Integer, db.ForeignKey('superficie.id'))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self): # pragma: no cover
        return '<Radiometria %r>' % (str(self.id))

# Tabla Superficie
class Superficie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    radiometrias = db.relationship('Radiometria', backref='superficie_radiometria', lazy='dynamic',
                                   cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def has_radiometria(self, radiometria):
        return self.radiometrias.filter(radiometria.id_superficie == self.id).count() > 0

    def add_radiometria(self, radiometria):
        if not self.has_radiometria(radiometria):
            self.radiometrias.append(radiometria)
            return self

    def get_radiometrias(self):
        return Radiometria.query.filter(Radiometria.id_superficie == self.id).all()

    def __repr__(self): # pragma: no cover
        return '<Superficie %r>' % (self.nombre)
''' ------- '''


# Creamos la tabla "seguidores" para asociación muchos-a-muchos y autorreferenciada en usuario
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# Entidad Usuario con sus respectivos métodos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    nombre = db.Column(db.String(180))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    descargas = db.relationship('Descarga', backref='descarga', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    editar = db.Column(db.Boolean)
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
        return re.sub('[^a-zA-Z0-9_\.\s]', '', nickname)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_editable(self):
        return self.editar

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

# Entidad Descarga para control de informacion
class Descarga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'))
    institucion = db.Column(db.String(120))
    fecha_descarga = db.Column(db.DateTime)
    nombre_archivo = db.Column(db.String(120))
    tamanio_archivo = db.Column(db.DECIMAL(precision=30, scale=3))

    def agregar(self, email, folder, filename):
        self.id_usuario = User.query.filter_by(email=email).first().id
        self.institucion = email.split('@')[1].split('.')[0].upper()
        self.fecha_descarga = datetime.utcnow()
        self.nombre_archivo = filename
        self.tamanio_archivo = os.path.getsize(os.path.join(folder, filename))
        try:
            db.session.add(self)
            db.session.commit()
        except:
            traceback.print_exc()
            db.session.rollback()

    def __repr__(self):
        return '<Descarga %r>' % (self.id)


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

