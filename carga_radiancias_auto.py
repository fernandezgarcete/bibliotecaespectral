from app import db
from app.models import Fotometria, Punto, Radiometria
from app.utils import find_pattern_files

__author__ = 'Juanjo'

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

archivo = '*FOT*'
raiz = 'C:/Users/Juanjo/Documents/Biblioteca de firmas espectrales/Campañas/'

camp = '56-20141215-HA/'
cob = '1-Cebolla-entablon_1216/'
f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P2')).first()
cargar_fotometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P4')).first()
cargar_fotometria(f[0], p4)

f_url = raiz + camp + cob + 'Punto5'
f = find_pattern_files(archivo, f_url)
p5 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P5')).first()
cargar_fotometria(f[0], p5)

f_url = raiz + camp + cob + 'Punto6'
f = find_pattern_files(archivo, f_url)
p6 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P6')).first()
cargar_fotometria(f[0], p6)

f_url = raiz + camp + cob + 'Punto7'
f = find_pattern_files(archivo, f_url)
p7 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P7')).first()
cargar_fotometria(f[0], p7)

f_url = raiz + camp + cob + 'Punto8'
f = find_pattern_files(archivo, f_url)
p8 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P8')).first()
cargar_fotometria(f[0], p8)

f_url = raiz + camp + cob + 'Punto9'
f = find_pattern_files(archivo, f_url)
p9 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P9')).first()
cargar_fotometria(f[0], p9)

f_url = raiz + camp + cob + 'Punto14'
f = find_pattern_files(archivo, f_url)
p14 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P14')).first()
cargar_fotometria(f[0], p14)

camp = '56-20141215-HA/'
cob = '1-Cebolla-temprana/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P1')).first()
cargar_fotometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P3')).first()
cargar_fotometria(f[0], p3)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p10 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P10')).first()
cargar_fotometria(f[0], p10)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p11 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P11')).first()
cargar_fotometria(f[0], p11)

f_url = raiz + camp + cob + 'Punto5'
f = find_pattern_files(archivo, f_url)
p12 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P12')).first()
cargar_fotometria(f[0], p12)

f_url = raiz + camp + cob + 'Punto6'
f = find_pattern_files(archivo, f_url)
p13 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P13')).first()
cargar_fotometria(f[0], p13)

f_url = raiz + camp + cob + 'Punto7-flor de cebolla'
f = find_pattern_files(archivo, f_url)
p15 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P15')).first()
cargar_fotometria(f[0], p15)

camp = '56-20141215-HA/'
cob = '1-Cebolla-temprana_12/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p16 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P16')).first()
cargar_fotometria(f[0], p16)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p17 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P17')).first()
cargar_fotometria(f[0], p17)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p18 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P18')).first()
cargar_fotometria(f[0], p18)

camp = '56-20141215-HA/'
cob = '2-Maiz_1218/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P1')).first()
cargar_fotometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P2')).first()
cargar_fotometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P3')).first()
cargar_fotometria(f[0], p3)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P4')).first()
cargar_fotometria(f[0], p4)

camp = '56-20141215-HA/'
cob = '3-Girasol_1218/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M3-GIRASOL-P1')).first()
cargar_fotometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M3-GIRASOL-P2')).first()
cargar_fotometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M3-GIRASOL-P3')).first()
cargar_fotometria(f[0], p3)

camp = '56-20141215-HA/'
cob = '4-Alfalfa_1217/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M4-ALFALFA-P1')).first()
cargar_fotometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M4-ALFALFA-P2')).first()
cargar_fotometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M4-ALFALFA-P3')).first()
cargar_fotometria(f[0], p3)

camp = '56-20141215-HA/'
cob = '5-Cebolla-morada-tardia_1217/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P1')).first()
cargar_fotometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P2')).first()
cargar_fotometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P3')).first()
cargar_fotometria(f[0], p3)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P4')).first()
cargar_fotometria(f[0], p4)

f_url = raiz + camp + cob + 'Punto5'
f = find_pattern_files(archivo, f_url)
p5 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P5')).first()
cargar_fotometria(f[0], p5)

f_url = raiz + camp + cob + 'Punto6'
f = find_pattern_files(archivo, f_url)
p6 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P6')).first()
cargar_fotometria(f[0], p6)


archivo = '*FOT*'
camp = '57-20150121-RU/'
f_url = raiz + camp + 'Punto-1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M1-RIO-P1')).first()
cargar_fotometria(f[0], p1)

f_url = raiz + camp + 'Punto-2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M2-RIO-P1')).first()
cargar_fotometria(f[0], p2)

f_url = raiz + camp + 'Punto-3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M3-RIO-P1')).first()
cargar_fotometria(f[0], p3)

f_url = raiz + camp + 'Punto-4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M4-RIO-P1')).first()
cargar_fotometria(f[0], p4)

f_url = raiz + camp + 'Punto-5'
f = find_pattern_files(archivo, f_url)
p5 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M5-RIO-P1')).first()
cargar_fotometria(f[0], p5)

f_url = raiz + camp + 'Punto-6'
f = find_pattern_files(archivo, f_url)
p6 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M6-RIO-P1')).first()
cargar_fotometria(f[0], p6)

f_url = raiz + camp + 'Punto-7'
f = find_pattern_files(archivo, f_url)
p7 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M7-RIO-P1')).first()
cargar_fotometria(f[0], p7)

f_url = raiz + camp + 'Punto-8'
f = find_pattern_files(archivo, f_url)
p8 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M8-RIO-P1')).first()
cargar_fotometria(f[0], p8)


def cargar_radiometria(uri, punto):
    file = open(uri, 'r')
    for i, line in enumerate(file):
        if i > 0 and line != '\n':
            rad = Radiometria()
            s1 = line.split(' ')
            s2 = s1[0].split('\t')
            s1 = line.split(' ')
            r = s1[1].replace(',', '.')
            w = s2[0]
            rad.longitud_onda = float(w)
            rad.radiancia = float(r)
            rad.id_punto = punto.id
            db.session.add(rad)
            db.session.commit()
            print(w+'-'+r)
    file.close()

archivo = '*rad.txt*'
raiz = 'C:/Users/Juanjo/Documents/Biblioteca de firmas espectrales/Campañas/'

camp = '56-20141215-HA/'
cob = '1-Cebolla-entablon_1216/'
f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P2')).first()
cargar_radiometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P4')).first()
cargar_radiometria(f[0], p4)

f_url = raiz + camp + cob + 'Punto5'
f = find_pattern_files(archivo, f_url)
p5 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P5')).first()
cargar_radiometria(f[0], p5)

f_url = raiz + camp + cob + 'Punto6'
f = find_pattern_files(archivo, f_url)
p6 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P6')).first()
cargar_radiometria(f[0], p6)

f_url = raiz + camp + cob + 'Punto7'
f = find_pattern_files(archivo, f_url)
p7 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P7')).first()
cargar_radiometria(f[0], p7)

f_url = raiz + camp + cob + 'Punto8'
f = find_pattern_files(archivo, f_url)
p8 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P8')).first()
cargar_radiometria(f[0], p8)

f_url = raiz + camp + cob + 'Punto9'
f = find_pattern_files(archivo, f_url)
p9 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P9')).first()
cargar_radiometria(f[0], p9)

f_url = raiz + camp + cob + 'Punto14'
f = find_pattern_files(archivo, f_url)
p14 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P14')).first()
cargar_radiometria(f[0], p14)

camp = '56-20141215-HA/'
cob = '1-Cebolla-temprana/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P1')).first()
cargar_radiometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P3')).first()
cargar_radiometria(f[0], p3)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p10 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P10')).first()
cargar_radiometria(f[0], p10)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p11 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P11')).first()
cargar_radiometria(f[0], p11)

f_url = raiz + camp + cob + 'Punto5'
f = find_pattern_files(archivo, f_url)
p12 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P12')).first()
cargar_radiometria(f[0], p12)

f_url = raiz + camp + cob + 'Punto6'
f = find_pattern_files(archivo, f_url)
p13 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P13')).first()
cargar_radiometria(f[0], p13)

f_url = raiz + camp + cob + 'Punto7-flor de cebolla'
f = find_pattern_files(archivo, f_url)
p15 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P15')).first()
cargar_radiometria(f[0], p15)

camp = '56-20141215-HA/'
cob = '1-Cebolla-temprana_12/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p16 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P16')).first()
cargar_radiometria(f[0], p16)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p17 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P17')).first()
cargar_radiometria(f[0], p17)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p18 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P18')).first()
cargar_radiometria(f[0], p18)

camp = '56-20141215-HA/'
cob = '2-Maiz_1218/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P1')).first()
cargar_radiometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P2')).first()
cargar_radiometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P3')).first()
cargar_radiometria(f[0], p3)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M2-MAIZ-P4')).first()
cargar_radiometria(f[0], p4)

camp = '56-20141215-HA/'
cob = '3-Girasol_1218/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M3-GIRASOL-P1')).first()
cargar_radiometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M3-GIRASOL-P2')).first()
cargar_radiometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M3-GIRASOL-P3')).first()
cargar_radiometria(f[0], p3)

camp = '56-20141215-HA/'
cob = '4-Alfalfa_1217/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M4-ALFALFA-P1')).first()
cargar_radiometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M4-ALFALFA-P2')).first()
cargar_radiometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M4-ALFALFA-P3')).first()
cargar_radiometria(f[0], p3)

camp = '56-20141215-HA/'
cob = '5-Cebolla-morada-tardia_1217/'
f_url = raiz + camp + cob + 'Punto1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P1')).first()
cargar_radiometria(f[0], p1)

f_url = raiz + camp + cob + 'Punto2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P2')).first()
cargar_radiometria(f[0], p2)

f_url = raiz + camp + cob + 'Punto3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P3')).first()
cargar_radiometria(f[0], p3)

f_url = raiz + camp + cob + 'Punto4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P4')).first()
cargar_radiometria(f[0], p4)

f_url = raiz + camp + cob + 'Punto5'
f = find_pattern_files(archivo, f_url)
p5 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P5')).first()
cargar_radiometria(f[0], p5)

f_url = raiz + camp + cob + 'Punto6'
f = find_pattern_files(archivo, f_url)
p6 = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M5-CEBOLLA-MORADA-P6')).first()
cargar_radiometria(f[0], p6)


camp = '57-20150121-RU/'
f_url = raiz + camp + 'Punto-1'
f = find_pattern_files(archivo, f_url)
p1 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M1-RIO-P1')).first()
cargar_radiometria(f[0], p1)

f_url = raiz + camp + 'Punto-2'
f = find_pattern_files(archivo, f_url)
p2 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M2-RIO-P1')).first()
cargar_radiometria(f[0], p2)

f_url = raiz + camp + 'Punto-3'
f = find_pattern_files(archivo, f_url)
p3 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M3-RIO-P1')).first()
cargar_radiometria(f[0], p3)

f_url = raiz + camp + 'Punto-4'
f = find_pattern_files(archivo, f_url)
p4 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M4-RIO-P1')).first()
cargar_radiometria(f[0], p4)

f_url = raiz + camp + 'Punto-5'
f = find_pattern_files(archivo, f_url)
p5 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M5-RIO-P1')).first()
cargar_radiometria(f[0], p5)

f_url = raiz + camp + 'Punto-6'
f = find_pattern_files(archivo, f_url)
p6 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M6-RIO-P1')).first()
cargar_radiometria(f[0], p6)

f_url = raiz + camp + 'Punto-7'
f = find_pattern_files(archivo, f_url)
p7 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M7-RIO-P1')).first()
cargar_radiometria(f[0], p7)

f_url = raiz + camp + 'Punto-8'
f = find_pattern_files(archivo, f_url)
p8 = Punto.query.filter(Punto.nombre.like('%20150121-RIOURUGUAY-M8-RIO-P1')).first()
cargar_radiometria(f[0], p8)
