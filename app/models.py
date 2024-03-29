# -*- coding: utf-8 -*-
from datetime import datetime
import os
import traceback

__author__ = 'Juanjo'

from hashlib import md5
from app import db, app
from geoalchemy2 import Geometry
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
        elif res is None:
            res = db.engine.execute("SELECT ST_Contains(geom, punto) "
                                    "FROM (SELECT ST_SetSRID(ST_MakePoint("+lng+","+lat+"),4326) AS punto, "
                                    "geom FROM limite_arg) AS result;").fetchone()
            if res[0]:
                geom = db.engine.execute("SELECT ST_SetSRID(ST_MakePoint("+lng+","+lat+"),4326) AS result;").fetchone()
                loc = self.query.filter_by(geom=geom[0]).first()
                if loc is None:
                    self.nombre = nombre
                    self.nombre_dpto = nombre
                    self.nombre_prov = nombre
                    self.geom = geom[0]
                    db.session.add(self)
                    db.session.commit()
                    return True
                elif loc is not None:
                    return 'Ya existe'
                else:
                    return False
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
            proyecto.nombre = form.nombre.data.upper()
            proyecto.descripcion = str(form.descripcion.data).replace('\r\n', ' ')
            proyecto.responsables = form.responsables.data
            proyecto.status = bool(form.status.data)
        else:
            proyecto.nombre = form.nombre.data.upper()
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
    objetivo = db.Column(db.String(300))
    teledeteccion = db.Column(db.String(600))
    especialidad = db.Column(db.String(600))
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))
    muestras = db.relationship('Muestra', backref='campania_muestra', lazy='dynamic',
                                          cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    def agregar(self, form):
        camp = self
        if int(form.id.data) > 0:
            camp = self.query.filter_by(id=int(form.id.data)).first()
            camp.nombre = form.ncampania.data.upper()
            camp.fecha = form.nfecha.data
            camp.fecha_publicacion = form.nfecha_pub.data
            camp.responsables = form.nresponsable.data
            camp.id_localidad = form.nlocalidad.data
            camp.objetivo = str(form.nobjetivo.data).replace('\r\n', ' ')
            camp.teledeteccion = str(form.teledeteccion.data).replace('\r\n', ' ')
            camp.especialidad = str(form.especialidad.data).replace('\r\n', ' ')
            camp.id_proyecto = form.nproyecto.data
        else:
            loc = Localidad.query.filter_by(id=form.nlocalidad.data).first()
            camp.nombre = camp.nombre_camp(loc, form.nfecha.data).upper()
            camp.fecha = form.nfecha.data
            camp.fecha_publicacion = form.nfecha_pub.data
            camp.responsables = form.nresponsable.data
            camp.id_localidad = form.nlocalidad.data
            camp.objetivo = str(form.nobjetivo.data).replace('\r\n', ' ')
            camp.teledeteccion = str(form.teledeteccion.data).replace('\r\n', ' ')
            camp.especialidad = str(form.especialidad.data).replace('\r\n', ' ')
            camp.id_proyecto = form.nproyecto.data
        try:
            db.session.add(camp)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    # Crear nombre de la campaña
    def nombre_camp(self, loc, f):
        camps = self.query.filter_by(deleted=False).order_by('id').all()
        ult_id = 0
        l = ''
        # id campaña
        if len(camps) == 0:
            ult_id = '0001'
        elif len(camps) < 9:
            ult_id = camps[len(camps) - 1].id + 1
            ult_id = '000' + str(ult_id)
        elif len(camps) < 99:
            ult_id = camps[len(camps) - 1].id + 1
            ult_id = '00' + str(ult_id)
        elif len(camps) < 999:
            ult_id = camps[len(camps) - 1].id + 1
            ult_id = '0' + str(ult_id)
        elif len(camps) > 999:
            ult_id = camps[len(camps) - 1].id + 1
            ult_id = str(ult_id)
        # fecha
        y = str(f.year)
        m = str(f.month)
        d = str(f.day)
        if f.month < 10:
            m = '0' + str(f.month)
        if f.day < 10:
            d = '0' + str(f.day)
        f = y + m + d
        # localidad
        for c in camps:
            if c.id_localidad == loc.id:
                l = c.nombre.rsplit('-', 1)[1]
                break
        if l is '':
            l = loc.nombre.replace(' ', '_')
        return str(ult_id) + '-' + f + '-' + l

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_campania == self.id, Muestra.deleted == False).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_campania == self.id, Muestra.deleted == False).all()

    @property
    def is_complete(self):
        return True

    def __repr__(self): # pragma: no cover
        return '<Campaña %r>' % (self.nombre)

# Tabla Tipo de Cobertura
class TipoCobertura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fuente = db.Column(db.Integer, db.ForeignKey('fuente_datos.id'))
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    coberturas = db.relationship('Cobertura', backref='cobertura', lazy='dynamic',
                                 cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False
    
    def agregar(self, form):
        tp = self
        if int(form.id.data) > 0:
            tp = self.query.filter_by(id=int(form.id.data)).first()
            tp.id_fuente = int(form.id_fuente.data)
            tp.nombre = form.nombre.data.upper()
        else:
            tp.id_fuente = int(form.id_fuente.data)
            tp.nombre = form.nombre.data.upper()
        try:
            db.session.add(tp)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    def has_cobertura(self, cobertura):
        return self.coberturas.filter(cobertura.id_tipocobertura == self.id).count() > 0

    def add_cobertura(self, cobertura):
        if not self.has_cobertura(cobertura):
            self.coberturas.append(cobertura)
            return self

    def get_coberturas(self):
        return Cobertura.query.filter(Cobertura.id_tipocobertura == self.id, Cobertura.deleted == False).all()

    def __repr__(self): # pragma: no cover
        return '<Tipo de Cobertura %r>' % (self.nombre)


# Tabla Fuente de Datos
class FuenteDatos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    tipo_coberturas = db.relationship('TipoCobertura', backref='fuente', lazy='dynamic',
                                 cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def agregar(self, form):
        fd = self
        if int(form.id.data) > 0:
            fd = self.query.filter_by(id=int(form.id.data)).first()
            fd.nombre = form.nombre.data.upper()
        else:
            fd.nombre = form.nombre.data.upper()
        try:
            db.session.add(fd)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    def has_tipo_cobertura(self, tp):
        return self.coberturas.filter(tp.id_fuente == self.id).count() > 0

    def get_tipo_coberturas(self):
        return TipoCobertura.query.filter(TipoCobertura.id_fuente == self.id, TipoCobertura.deleted == False).all()

    def __repr__(self): # pragma: no cover
        return '<Fuente de Datos %r>' % (self.nombre)

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
    
    def agregar(self, form):
        cob = self
        if int(form.id.data) > 0:
            cob = self.query.filter_by(id=int(form.id.data)).first()
            cob.nombre = form.nombre.data.upper()
            cob.id_tipocobertura = int(form.tipo_cobertura.data)
            cob.altura = float(form.altura.data)
            cob.fenologia = str(form.fenologia.data).replace('\r\n', ' ')
            cob.observaciones = str(form.observaciones.data).replace('\r\n', ' ')
        else:
            cob.nombre = form.nombre.data.upper()
            cob.id_tipocobertura = int(form.tipo_cobertura.data)
            cob.altura = float(form.altura.data)
            cob.fenologia = str(form.fenologia.data).replace('\r\n', ' ')
            cob.observaciones = str(form.observaciones.data).replace('\r\n', ' ')
        try:
            db.session.add(cob)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_cobertura == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_cobertura == self.id, Muestra.deleted == False).all()

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

    def agregar(self, form):
        muestra = self
        if int(form.id.data) > 0:
            muestra = self.query.filter_by(id=int(form.id.data)).first()
            muestra.nombre = form.nombre.data.upper()
            muestra.operador = form.operador.data
            muestra.id_cobertura = int(form.cobertura.data)
            muestra.id_campania = int(form.campania.data)
            muestra.id_metodologia = int(form.metodologia.data)
            muestra.id_radiometro = int(form.radiometro.data)
            muestra.id_camara = int(form.camara.data)
            muestra.id_gps = int(form.gps.data)
            muestra.id_fotometro = int(form.fotometro.data)
            muestra.id_patron = int(form.espectralon.data)
        else:
            cob = Cobertura.query.filter_by(id=form.cobertura.data).first()
            camp = Campania.query.filter_by(id=int(form.campania.data)).first()
            muestra.nombre = muestra.nombre_muestra(camp, cob).upper()
            muestra.operador = form.operador.data
            muestra.id_cobertura = int(form.cobertura.data)
            muestra.id_campania = int(form.campania.data)
            muestra.id_metodologia = int(form.metodologia.data)
            muestra.id_radiometro = int(form.radiometro.data)
            muestra.id_camara = int(form.camara.data)
            muestra.id_gps = int(form.gps.data)
            muestra.id_fotometro = int(form.fotometro.data)
            muestra.id_patron = int(form.espectralon.data)
        try:
            db.session.add(muestra)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    # Crear nombre de la muestra
    def nombre_muestra(self, campania, cobertura):
        m = self.query.filter_by(id_campania=campania.id).count()
        ult_id = 0
        if m == 0:
            ult_id = '1'
        if m > 0:
            ult_id = m + 1
        return campania.nombre + '-M' + str(ult_id) + '-' + cobertura.nombre

    def has_punto(self, punto):
        return self.coberturas.filter(punto.id_muestra == self.id).count() > 0

    def add_punto(self, punto):
        if not self.has_punto(punto):
            self.puntos.append(punto)
            return self

    def get_puntos(self):
        return Punto.query.filter(Punto.id_muestra == self.id, Punto.deleted == False).order_by('id').all()

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

    def agregar(self, form):
        camara = self
        if int(form.id.data) > 0:
            camara = self.query.filter_by(id=int(form.id.data)).first()
            camara.codigo = form.codigo.data.upper()
            camara.nombre = form.nombre.data.upper()
            camara.marca = form.marca.data
            camara.modelo = form.modelo.data
            camara.nro_serie = form.nro_serie.data
            camara.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        else:
            camara.codigo = form.codigo.data.upper()
            camara.nombre = form.nombre.data.upper()
            camara.marca = form.marca.data
            camara.modelo = form.modelo.data
            camara.nro_serie = form.nro_serie.data
            camara.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        try:
            db.session.add(camara)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False
        
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
        return Muestra.query.filter(Muestra.id_camara == self.id, Muestra.deleted == False).all()

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
    
    def agregar(self, form):
        gps = self
        if int(form.id.data) > 0:
            gps = self.query.filter_by(id=int(form.id.data)).first()
            gps.codigo = form.codigo.data.upper()
            gps.nombre = form.nombre.data.upper()
            gps.marca = form.marca.data
            gps.modelo = form.modelo.data
            gps.nro_serie = form.nro_serie.data
            gps.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        else:
            gps.codigo = form.codigo.data.upper()
            gps.nombre = form.nombre.data.upper()
            gps.marca = form.marca.data
            gps.modelo = form.modelo.data
            gps.nro_serie = form.nro_serie.data
            gps.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        try:
            db.session.add(gps)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False
        
    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False
    
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
        return Muestra.query.filter(Muestra.id_gps == self.id, Muestra.deleted == False).all()

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
    
    def agregar(self, form):
        fotometro = self
        if int(form.id.data) > 0:
            fotometro = self.query.filter_by(id=int(form.id.data)).first()
            fotometro.codigo = form.codigo.data.upper()
            fotometro.nombre = form.nombre.data.upper()
            fotometro.marca = form.marca.data
            fotometro.modelo = form.modelo.data
            fotometro.nro_serie = form.nro_serie.data
            fotometro.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        else:
            fotometro.codigo = form.codigo.data.upper()
            fotometro.nombre = form.nombre.data.upper()
            fotometro.marca = form.marca.data
            fotometro.modelo = form.modelo.data
            fotometro.nro_serie = form.nro_serie.data
            fotometro.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        try:
            db.session.add(fotometro)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False
        
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

    def agregar(self, form):
        patron = self
        if int(form.id.data) > 0:
            patron = self.query.filter_by(id=int(form.id.data)).first()
            patron.codigo = form.codigo.data.upper()
            patron.nombre = form.nombre.data.upper()
            patron.marca = form.marca.data
            patron.modelo = form.modelo.data
            patron.nro_serie = form.nro_serie.data
            patron.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        else:
            patron.codigo = form.codigo.data.upper()
            patron.nombre = form.nombre.data.upper()
            patron.marca = form.marca.data
            patron.modelo = form.modelo.data
            patron.nro_serie = form.nro_serie.data
            patron.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        try:
            db.session.add(patron)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

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
        return Muestra.query.filter(Muestra.id_patron == self.id, Muestra.deleted == False).all()

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
    noise_equivalence_radiance_vnir = db.Column(db.String(120))
    noise_equivalence_radiance_swir1 = db.Column(db.String(120))
    noise_equivalence_radiance_swir2 = db.Column(db.String(120))
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

    def agregar(self, form):
        rad = self
        if int(form.id.data) > 0:
            rad = self.query.filter_by(id=int(form.id.data)).first()
            rad.codigo = form.codigo.data.upper()
            rad.nombre = form.nombre.data.upper()
            rad.marca = form.marca.data
            rad.modelo = form.modelo.data
            rad.nro_serie = form.nro_serie.data
            rad.rango_espectral = form.rango_espectral.data
            rad.resolucion_espectral = form.resolucion_espectral.data
            rad.ancho_banda = form.ancho_banda.data
            rad.tiempo_escaneo = float(form.tiempo_escaneo.data)
            rad.reproducibilidad_ancho_banda = float(form.reproducibilidad.data)
            rad.exactitud_ancho_banda = float(form.exactitud.data)
            rad.detector_vnir = form.detector_vnir.data
            rad.detector_swir1 = form.detector_swir1.data
            rad.detector_swir2 = form.detector_swir2.data
            rad.noise_equivalence_radiance_vnir = form.noise_vnir.data
            rad.noise_equivalence_radiance_swir1 = form.noise_swir1.data
            rad.noise_equivalence_radiance_swir2 = form.noise_swir2.data
            rad.largo_fibra_optica = float(form.largo_fibra.data)
            rad.fov = float(form.fov.data)
            rad.fov_cosenoidal = form.fov_cosenoidal.data
            rad.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        else:
            rad.codigo = form.codigo.data.upper()
            rad.nombre = form.nombre.data.upper()
            rad.marca = form.marca.data
            rad.modelo = form.modelo.data
            rad.nro_serie = form.nro_serie.data
            rad.rango_espectral = form.rango_espectral.data
            rad.resolucion_espectral = form.resolucion_espectral.data
            rad.ancho_banda = form.ancho_banda.data
            rad.tiempo_escaneo = float(form.tiempo_escaneo.data)
            rad.reproducibilidad_ancho_banda = float(form.reproducibilidad.data)
            rad.exactitud_ancho_banda = float(form.exactitud.data)
            rad.detector_vnir = form.detector_vnir.data
            rad.detector_swir1 = form.detector_swir1.data
            rad.detector_swir2 = form.detector_swir2.data
            rad.noise_equivalence_radiance_vnir = form.noise_vnir.data
            rad.noise_equivalence_radiance_swir1 = form.noise_swir1.data
            rad.noise_equivalence_radiance_swir2 = form.noise_swir2.data
            rad.largo_fibra_optica = float(form.largo_fibra.data)
            rad.fov = float(form.fov.data)
            rad.fov_cosenoidal = form.fov_cosenoidal.data
            rad.accesorio = str(form.accesorio.data).replace('\r\n', ' ')
        try:
            db.session.add(rad)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    def has_muestra(self, muestra):
        return self.muestras.filter(muestra.id_radiometro == self.id).count() > 0

    def add_muestra(self, muestra):
        if not self.has_muestra(muestra):
            self.muestras.append(muestra)
            return self

    def get_muestras(self):
        return Muestra.query.filter(Muestra.id_radiometro == self.id, Muestra.deleted == False).all()

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
        return Muestra.query.filter(Muestra.id_metodologia == self.id, Muestra.deleted == False).all()

    def __repr__(self): # pragma: no cover
        return '<Metodología %r>' % (self.nombre)

    def agregar(self, form):
        metod = self
        if int(form.id.data) > 0:
            metod = self.query.filter_by(id=int(form.id.data)).first()
            metod.nombre = form.nombre.data.upper()
            metod.descripcion = str(form.descripcion.data).replace('\r\n', ' ')
            metod.metodologia_medicion = str(form.medicion.data).replace('\r\n', ' ')
            metod.angulo_cenital = int(form.cenit.data)
            metod.angulo_azimutal = int(form.azimut.data)
        else:
            metod.nombre = form.nombre.data.upper()
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
    foto = db.Column(db.String(600))
    id_muestra = db.Column(db.Integer, db.ForeignKey('muestra.id'))
    radiometrias = db.relationship('Radiometria', backref='punto_radiometria', lazy='dynamic',
                                   cascade="save-update, merge, delete")
    fotometrias = db.relationship('Fotometria', backref='Fotometria', lazy='dynamic',
                                  cascade="save-update, merge, delete")
    productos_radiancias = db.relationship('Reflectancia', backref='producto_radiancia_punto', lazy='dynamic',
                                           cascade="save-update, merge, delete")
    deleted = db.Column(db.Boolean, default=False)

    def agregar(self, form):
        punto = self
        lat = form.lat_long.data.split('(')[1].split(',')[0]
        lng = form.lat_long.data.split(' ')[1].split(')')[0]
        point = db.engine.execute('SELECT ST_SetSRID(ST_MakePoint('+lat+', '+lng+'), 4326)').fetchone()[0]
        if int(form.id.data) > 0:
            punto = self.query.filter_by(id=int(form.id.data)).first()
            punto.nombre = form.nombre.data.upper()
            punto.fecha_hora = form.fecha_hora.data
            punto.geom = point
            punto.altura_medicion = float(form.altura.data)
            punto.presion = float(form.presion.data)
            punto.temperatura = float(form.temp.data)
            punto.nubosidad = int(form.nubosidad.data)
            punto.cantidad_tomas = int(form.cant_tomas.data)
            punto.id_muestra = int(form.muestra.data)
            punto.viento_direccion = form.dir_viento.data
            punto.viento_velocidad = form.vel_viento.data
            punto.foto = form.foto.data
            punto.oleaje = form.oleaje.data
            punto.estado = form.estado.data
            punto.observaciones = str(form.obs.data).replace('\r\n', ' ')
        else:
            mues = Muestra.query.filter_by(id=form.muestra.data).first()
            punto.nombre = punto.nombre_punto(mues).upper()
            punto.fecha_hora = form.fecha_hora.data
            punto.geom = point
            punto.altura_medicion = float(form.altura.data)
            punto.presion = float(form.presion.data)
            punto.temperatura = float(form.temp.data)
            punto.nubosidad = int(form.nubosidad.data)
            punto.cantidad_tomas = int(form.cant_tomas.data)
            punto.id_muestra = int(form.muestra.data)
            punto.viento_direccion = form.dir_viento.data
            punto.viento_velocidad = form.vel_viento.data
            punto.foto = form.foto.data
            punto.oleaje = form.oleaje.data
            punto.estado = form.estado.data
            punto.observaciones = str(form.obs.data).replace('\r\n', ' ')
        try:
            db.session.add(punto)
            db.session.commit()
            return True
        except:
            traceback.print_exc()
            db.session.rollback()
            return False

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    # Crear nombre del punto
    def nombre_punto(self, muestra):
        p = self.query.filter_by(id_muestra=muestra.id).count()
        ult_id = 0
        if p == 0:
            ult_id = '1'
        if p > 0:
            ult_id = p + 1
        return muestra.nombre + '-P' + str(ult_id)

    def has_radiometria(self, radiometria):
        return self.radiometrias.filter(radiometria.id_punto == self.id).count() > 0

    def add_radiometria(self, radiometria):
        if not self.has_radiometria(radiometria):
            self.radiometrias.append(radiometria)
            return self

    def get_radiometrias(self):
        return Radiometria.query.filter(Radiometria.id_punto == self.id, Radiometria.deleted == False).all()

    def has_fotometria(self, fotometria):
        return self.fotometrias.filter(fotometria.id_punto == self.id).count() > 0

    def add_fotometria(self, fotometria):
        if not self.has_fotometria(fotometria):
            self.fotometrias.append(fotometria)
            return self

    def get_fotometrias(self):
        return Fotometria.query.filter(Fotometria.id_punto == self.id, Fotometria.deleted == False).all()

    def has_producto_radiancia(self, producto_radiancia):
        return self.productos_radiancias.filter(producto_radiancia.id_punto == self.id).count() > 0

    def add_producto_radiancia(self, producto_radiancia):
        if not self.has_producto_radiancia(producto_radiancia):
            self.productos_radiancias.append(producto_radiancia)
            return self

    def get_productos_radiancias(self):
        return Reflectancia.query.filter(Reflectancia.id_punto == self.id, Reflectancia.deleted == False).all()

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
    archivo = db.Column(db.String(120))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self): # pragma: no cover
        return '<Fotometria %r>' % (str(self.id))

# Tabla Reflectancia
class Reflectancia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    reflectancia = db.Column(db.DECIMAL(precision=20, scale=15))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    archivo = db.Column(db.String(120))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self):     # pragma: no cover
        return '<Reflectancia %r>' % (str(self.id))

# Tabla Reflectancia AVG
class ReflectanciaAvg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    reflectancia = db.Column(db.DECIMAL(precision=20, scale=15))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    archivo = db.Column(db.String(120))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self):     # pragma: no cover
        return '<Reflectancia AVG %r>' % (str(self.id))

# Tabla Reflectancia
class ReflectanciaStd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    reflectancia = db.Column(db.DECIMAL(precision=20, scale=15))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    archivo = db.Column(db.String(120))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self):     # pragma: no cover
        return '<Reflectancia STD %r>' % (str(self.id))

# Tabla Radiancia Avg
class RadianciaAvg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    radiancia_avg = db.Column(db.DECIMAL(precision=20, scale=15))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    archivo = db.Column(db.String(120))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self):     # pragma: no cover
        return '<Radiancia AVG %r>' % (str(self.id))


# Tabla Radiancia Std
class RadianciaStd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    radiancia_std = db.Column(db.DECIMAL(precision=20, scale=15))
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    archivo = db.Column(db.String(120))
    deleted = db.Column(db.Boolean, default=False)

    @property
    def is_deleted(self):
        if self.deleted is True:
            return True
        return False

    def __repr__(self):     # pragma: no cover
        return '<Radiancia STD %r>' % (str(self.id))


# Tabla Radiometria
class Radiometria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud_onda = db.Column(db.Integer)
    radiancia = db.Column(db.DECIMAL(precision=20, scale=15))
    toma = db.Column(db.Integer)
    id_punto = db.Column(db.Integer, db.ForeignKey('punto.id'))
    id_superficie = db.Column(db.Integer, db.ForeignKey('superficie.id'))
    archivo = db.Column(db.String(120))
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
        return Radiometria.query.filter(Radiometria.id_superficie == self.id, Radiometria.deleted == False).all()

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
        self.institucion = email.split('@')[1].upper()
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

