from datetime import datetime
import fnmatch
import os
import traceback
from app import db
from .models import Fotometria, Punto, Radiometria, Reflectancia, RadianciaAvg, RadianciaStd

__author__ = 'Juanjo'

def cargar_fotometria(uri, punto, archivo):
    try:
        with open(uri, 'r') as f:
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
                    fot.archivo = archivo
                    db.session.add(fot)
                    db.session.commit()
        print('Archivo cargado : %s' % archivo)
        print(datetime.now())
    except:
        traceback.print_exc()
        db.session.rollback()
        return False


def cargar_radiometria(uri, punto, archivo):
    try:
        with open(uri, 'r') as file:
            file.readline()
            for line in file:
                rad = Radiometria()
                ref = line.split('\t')
                rad.longitud_onda = int(ref[0])
                rad.radiancia = float(ref[1].replace(',', '.'))
                rad.id_punto = punto.id
                rad.archivo = archivo
                db.session.add(rad)
                db.session.commit()
        print('Archivo cargado : %s' % archivo)
        print(datetime.now())
    except:
        traceback.print_exc()
        db.session.rollback()
        return False


# Carga de Reflectancia, Radiancia Avg o Radiancia Std
def cargar_prod_rad(ur1, punto, archivo, producto):
    try:
        with open(ur1, 'r') as file1:
            file1.readline()
            for line in file1:
                if producto == 'ref':
                    prod = Reflectancia()
                    ref = line.split('\t')
                    prod.longitud_onda = int(ref[0])
                    prod.reflectancia = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
                elif producto == 'radavg':
                    prod = RadianciaAvg()
                    ref = line.split('\t')
                    prod.longitud_onda = int(ref[0])
                    prod.radiancia_avg = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
                else:
                    prod = RadianciaStd()
                    ref = line.split('\t')
                    prod.longitud_onda = int(ref[0])
                    prod.radiancia_std = float(ref[1].replace(',', '.'))
                    prod.id_punto = punto.id
                    prod.archivo = archivo
                    db.session.add(prod)
                    db.session.commit()
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
        elif folder == 'rad':
            Radiometria.query.filter(Radiometria.id_punto == punto.id, Radiometria.archivo == f).delete()
            db.session.commit()
        elif folder == 'fot':
            Fotometria.query.filter(Fotometria.id_punto == punto.id, Fotometria.archivo == f).delete()
            db.session.commit()
