# -*- coding: utf-8 -*-
from app.models import Campania, Muestra, Punto

__author__ = 'Juanjo'
from datetime import datetime
import os

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
    elif tipo == 'ref':
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
