# -*- coding: utf-8 -*-
import fnmatch
import os
from app import db
from app.models import Campania, Muestra, Punto, Fotometria

__author__ = 'Juanjo'
from datetime import datetime


def cargar_archivo(lugar, name, tipo, archivo):
    if tipo == 'rad':
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            archivo.save(os.path.join(lugar, name))
        except:
            raise
        return 1
    elif tipo == 'radavg':
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            archivo.save(os.path.join(lugar, name))
        except:
            raise
        return 2
    elif tipo == 'radstd':
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            archivo.save(os.path.join(lugar, name))
        except:
            raise
        return 3
    elif tipo == 'ref1':
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            archivo.save(os.path.join(lugar, name))
        except:
            raise
        return 4
    elif tipo == 'refavg':
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            archivo.save(os.path.join(lugar, name))
        except:
            raise
        return 5
    elif tipo == 'refstd':
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            archivo.save(os.path.join(lugar, name))
        except:
            raise
        return 6
    elif tipo == 'img':
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            archivo.save(os.path.join(lugar, name))
        except:
            raise
        return 7
    else:
        return False


def nombre_camp(loc, f):
    camps = Campania.query.all()
    ult_id = 0
    l = ''
    # id campaña
    if len(camps) == 0:
        ult_id = '001'
    elif len(camps) < 10:
        ult_id = camps[len(camps)-1].id + 1
        ult_id = '00'+str(ult_id)
    elif len(camps) < 100:
        ult_id = camps[len(camps)-1].id + 1
        ult_id = '0'+str(ult_id)
    # fecha
    y = str(f.year)
    m = str(f.month)
    d = str(f.day)
    if f.month < 10:
        m = '0'+str(f.month)
    if f.day < 10:
        d = '0'+str(f.day)
    f = y+m+d
    # localidad
    for c in camps:
        if c.id_localidad == loc.id:
            l = c.nombre.rsplit('-', 1)[1]
            break
    if l is '':
        locs = loc.nombre.split(' ')
        for ls in locs:
            l += ls

    return str(ult_id)+'-'+f+'-'+l


def nombre_muestra(campania, cobertura):
    m = Muestra.query.filter(Muestra.id_campania == campania.id).count()
    ult_id = 0
    if m == 0:
        ult_id = '1'
    if m > 0:
        ult_id = m + 1
    return campania.nombre+'-M'+str(ult_id)+'-'+cobertura.nombre


def nombre_punto(muestra):
    p = Punto.query.filter(Punto.id_muestra == muestra.id).count()
    ult_id = 0
    if p == 0:
        ult_id = '1'
    if p > 0:
        ult_id = p + 1
    return muestra.nombre+'-P'+str(ult_id)


# Buscar archivo
def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# Buscar todos los archivos con el mismo nombre
def find_all_files(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


# Buscar archivos con patron de nombre
def find_pattern_files(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


# Cargar de archivo Fotometria
def cargar_fotometria(uri, punto):
    f = open(uri, 'r')
    for i, line in enumerate(f):
        if i == 1:
            print(line.split(',')[25:39])
        if i > 1 and line != '\n':
            fot = Fotometria()
            v = line.split(',')
            fot.sig380 = float(v[25])
            fot.sig500 = float(v[26])
            fot.sig675 = float(v[27])
            fot.sig870 = float(v[28])
            fot.sig1020 = float(v[29])
            fot.std380 = float(v[30])
            fot.std500 = float(v[31])
            fot.std675 = float(v[32])
            fot.std870 = float(v[33])
            fot.std1020 = float(v[34])
            fot.r380 = float(v[35])
            fot.r500 = float(v[36])
            fot.r675 = float(v[37])
            fot.r870 = float(v[38])
            fot.r1020 = float(v[39])
            fot.id_punto = punto.id
            db.session.add(fot)
            db.session.commit()
            print(v[25:39])
    f.close()
