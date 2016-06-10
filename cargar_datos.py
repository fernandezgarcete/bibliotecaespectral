#!virtual/bin/python3
# -*- coding: utf-8 -*-
from datetime import date
from app import db
from app.models import Localidad, Campania
from app.utils import nombre_camp

__author__ = 'Juanjo'

l1 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2011, 2, 10)
n = nombre_camp(l1, f)
c1 = Campania(nombre=n, fecha=f, responsable=['Christian Weber', 'Martin Sandoval', 'Anabel Lamaro'], id_localidad=l1.id)
db.session.add(c1)
db.session.commit()

l2 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 17)
n = nombre_camp(l2, f)
c2 = Campania(nombre=n, fecha=f, responsable=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero'], id_localidad=l2.id)
db.session.add(c2)
db.session.commit()

l3 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 18)
n = nombre_camp(l3, f)
c3 = Campania(nombre=n, fecha=f, responsable=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero'], id_localidad=l3.id)
db.session.add(c3)
db.session.commit()

l4 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 25)
n = nombre_camp(l4, f)
c4 = Campania(nombre=n, fecha=f, responsable=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero',
                                              'Maximiliano Pisano'], id_localidad=l4.id)
db.session.add(c4)
db.session.commit()

l5 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 26)
n = nombre_camp(l5, f)
c5 = Campania(nombre=n, fecha=f, responsable=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero',
                                              'Maximiliano Pisano'], id_localidad=l5.id)
db.session.add(c5)
db.session.commit()

l6 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2011, 5, 10)
n = nombre_camp(l6, f)
c6 = Campania(nombre=n, fecha=f, responsable=['Maximiliano Guido', 'Guillermo Ibañez', 'Anabel Lamaro',
                                              'Claudio Sanchez', 'Nicolas Soldati'], id_localidad=l6.id)
db.session.add(c6)
db.session.commit()

l7 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2011, 9, 20)
n = nombre_camp(l7, f)
c7 = Campania(nombre=n, fecha=f, responsable=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero'], id_localidad=l7.id)
db.session.add(c7)
db.session.commit()

l8 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2011, 10, 31)
n = nombre_camp(l8, f)
c8 = Campania(nombre=n+'-AYSA-CCLORO', fecha=f, responsable=['Juan Cobo', 'Maximiliano Guido', 'Mariana Horlent',
                                                             'Anabel Lamaro', 'Carolina Fernández'], id_localidad=l8.id)
db.session.add(c8)
db.session.commit()

l9 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2011, 12, 1)
n = nombre_camp(l9, f)
c9 = Campania(nombre=n+'-AYSA-CCIANO', fecha=f, responsable=['Juan Cobo', 'Maximiliano Guido', 'Mariana Horlent',
                                                             'Anabel Lamaro', 'Carolina Fernández'], id_localidad=l9.id)
db.session.add(c9)
db.session.commit()

l10 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2011, 12, 1)
n = nombre_camp(l10, f)
c10 = Campania(nombre=n+'-AYSA-DIATOMEAS', fecha=f, responsable=['Juan Cobo', 'Maximiliano Guido', 'Mariana Horlent',
                                              'Anabel Lamaro', 'Carolina Fernández'], id_localidad=l10.id)
db.session.add(c10)
db.session.commit()

l11 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 12, 13)
n = nombre_camp(l11, f)
c11 = Campania(nombre=n, fecha=f, responsable=['Personal de CARU', 'Guillermo Ibañez', 'Andrea Drozd'], id_localidad=l11.id)
db.session.add(c11)
db.session.commit()

l12 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 12, 27)
n = nombre_camp(l12, f)
c12 = Campania(nombre=n, fecha=f, id_localidad=l12.id)
db.session.add(c12)
db.session.commit()

l13 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2012, 2, 1)
n = nombre_camp(l13, f)
c13 = Campania(nombre=n, fecha=f, responsable=['Juan Cobo', 'Nicolás Soldati', 'Claudio Sánchez',
                                               'Carolina Fernández'], id_localidad=l13.id)
db.session.add(c13)
db.session.commit()
