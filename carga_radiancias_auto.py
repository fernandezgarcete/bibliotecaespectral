from app import db
from app.models import Fotometria, Punto

__author__ = 'Juanjo'

f_url = 'C:/Users/Juanjo/Documents/Biblioteca de firmas espectrales/Campañas/56-20141215-HA/1-Cebolla-entablon_1216/' \
        'Punto2/Fototmetria/56-20151216-HA-FOT.txt'
f = open(f_url, 'r')
v = ''
punto = Punto.query.filter(Punto.nombre.like('%20141215-HILARIOASCASUBI-M1-CEBOLLA-P2')).first()
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
        id_punto=punto.id
        db.session.add(fot)
        db.session.commit()
        print(v[25:39])

f.close()


f1 = Fotometria(sig380=1.1234567,
                sig500=0,
                sig675=0,
                sig870=0,
                sig1020=0,
                std380=0,
                std500=0,
                std675=0,
                std870=0,
                std1020=0,
                std380=0,
                r380=0,
                r500=0,
                r675=0,
                r870=0,
                r1020=0,
                id_punto=punto.id)
