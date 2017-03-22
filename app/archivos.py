from datetime import datetime
import os
import traceback

from app import db
from .models import Fotometria, Punto, Radiometria, Reflectancia, RadianciaAvg, RadianciaStd, ReflectanciaStd, \
    ReflectanciaAvg

__author__ = 'Juanjo'

# Cargas de Fotometrías
def cargar_fotometria(uri, punto, archivo):
    try:
        with open(uri, 'r') as f:
            flag = False
            for i, line in enumerate(f):
                ls = line.split(',')
                if flag and line != '\n' and ls[0] != '':
                    fot = Fotometria()
                    v = ls
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
                    fot.archivo = archivo
                    db.session.add(fot)
                    db.session.commit()
                if ls[0].upper() == 'SN' and ls[1].upper() == 'DATE' and ls[2].upper() == 'TIME':
                    flag = True
        print('Archivo cargado : %s' % archivo)
        print(datetime.now())
    except:
        traceback.print_exc()
        db.session.rollback()
        return False

# Carga de Radiancias
def cargar_radiometria(uri, punto, archivo):
    try:
        with open(uri, 'r') as file:
            flag = False
            for line in file:
                ls = line.split('\t')
                if flag and ls[0] != '':
                    rad = Radiometria()
                    ref = ls
                    rad.longitud_onda = int(ref[0])
                    rad.radiancia = float(ref[1].replace(',', '.'))
                    rad.id_punto = punto.id
                    rad.archivo = archivo
                    db.session.add(rad)
                    db.session.commit()
                if ls[0] == 'Wavelength':
                    flag = True
        print('Archivo cargado : %s' % archivo)
        print(datetime.now())
    except:
        traceback.print_exc()
        db.session.rollback()
        return False


# Carga de Reflectancia, Reflectancia Avg, Reflectancia Std, Radiancia Avg o Radiancia Std
def cargar_prod_rad(ur1, punto, archivo, producto):
    try:
        with open(ur1, 'r') as file1:
            flag = False
            for line in file1:
                ls = line.split('\t')
                if producto == 'ref' and flag and ls[0] != '':
                    prod = Reflectancia()
                    ref = ls
                    prod.longitud_onda = int(ref[0])
                    prod.reflectancia = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
                if producto == 'radavg' and flag and ls[0] != '':
                    prod = RadianciaAvg()
                    ref = ls
                    prod.longitud_onda = int(ref[0])
                    prod.radiancia_avg = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
                if producto == 'radstd' and flag and ls[0] != '':
                    prod = RadianciaStd()
                    ref = ls
                    prod.longitud_onda = int(ref[0])
                    prod.radiancia_std = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
                if producto == 'refavg' and flag and ls[0] != '':
                    prod = ReflectanciaAvg()
                    ref = ls
                    prod.longitud_onda = int(ref[0])
                    prod.reflectancia = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
                if producto == 'refstd' and flag and ls[0] != '':
                    prod = ReflectanciaStd()
                    ref = ls
                    prod.longitud_onda = int(ref[0])
                    prod.reflectancia = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
                if ls[0] == 'Wavelength':
                    flag = True
        print('Archivo cargado : %s' % archivo)
        print(datetime.now())
    except:
        traceback.print_exc()
        db.session.rollback()
        return False


def guardar_archivo(file_url, idp):
    punto = Punto.query.filter(Punto.id == idp).first()
    folder = file_url.split(os.sep)
    if folder[len(folder)-2] == 'img':
        punto.foto += os.path.split(file_url)[1] + ','
        db.session.add(punto)
        db.session.commit()
        print('Archivo cargado : %s' % folder[len(folder)-1])
    elif folder[len(folder)-2] == 'rad':
        cargar_radiometria(file_url, punto, folder[len(folder)-1])
    elif folder[len(folder)-2] == 'ref':
        cargar_prod_rad(file_url, punto, folder[len(folder)-1], 'ref')
    elif folder[len(folder)-2] == 'radavg':
        cargar_prod_rad(file_url, punto, folder[len(folder)-1], 'radavg')
    elif folder[len(folder)-2] == 'radstd':
        cargar_prod_rad(file_url, punto, folder[len(folder)-1], 'radstd')
    elif folder[len(folder)-2] == 'refavg':
        cargar_prod_rad(file_url, punto, folder[len(folder)-1], 'refavg')
    elif folder[len(folder)-2] == 'refstd':
        cargar_prod_rad(file_url, punto, folder[len(folder)-1], 'refstd')
    else:
        cargar_fotometria(file_url, punto, folder[len(folder)-1])


def borrar_datos(path, files, idp):
    punto = Punto.query.filter(Punto.id == idp).first()
    folder = os.path.split(path)[1]
    if folder == 'img':
        borrar_imagenes(punto, files)
    else:
        borrar_prod_radiancia(punto, files, folder)
    for l in files:
        os.remove(os.path.join(path, l))


def borrar_imagenes(punto, files):
    fotos = list(set(punto.foto.split(',')) - set(files))
    punto.foto = ','.join(map(str, fotos)) + ','
    db.session.add(punto)
    db.session.commit()


def borrar_prod_radiancia(punto, files, folder):
    for f in files:
        if folder == 'ref':
            Reflectancia.query.filter(Reflectancia.id_punto == punto.id, Reflectancia.archivo == f).delete()
            db.session.commit()
        elif folder == 'radavg':
            RadianciaAvg.query.filter(RadianciaAvg.id_punto == punto.id, RadianciaAvg.archivo == f).delete()
            db.session.commit()
        elif folder == 'radstd':
            RadianciaStd.query.filter(RadianciaStd.id_punto == punto.id, RadianciaStd.archivo == f).delete()
            db.session.commit()
        elif folder == 'refavg':
            ReflectanciaAvg.query.filter(ReflectanciaAvg.id_punto == punto.id, ReflectanciaAvg.archivo == f).delete()
            db.session.commit()
        elif folder == 'refstd':
            ReflectanciaStd.query.filter(ReflectanciaStd.id_punto == punto.id, ReflectanciaStd.archivo == f).delete()
            db.session.commit()
        elif folder == 'rad':
            Radiometria.query.filter(Radiometria.id_punto == punto.id, Radiometria.archivo == f).delete()
            db.session.commit()
        elif folder == 'fot':
            Fotometria.query.filter(Fotometria.id_punto == punto.id, Fotometria.archivo == f).delete()
            db.session.commit()
