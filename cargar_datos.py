#!virtual/bin/python3
# -*- coding: utf-8 -*-
from datetime import date
from app import db
from app.models import Localidad, Campania, TipoCobertura, Cobertura, Instrumento
from app.utils import nombre_camp

__author__ = 'Juanjo'

# Carga de Tipos de Coberturas
tc1 = TipoCobertura(nombre='HIDROLOGIA')
tc2 = TipoCobertura(nombre='AGRICULTURA')
tc3 = TipoCobertura(nombre='CALIBRACION')
tc4 = TipoCobertura(nombre='LABORATORIO')
db.session.add(tc1)
db.session.add(tc2)
db.session.add(tc3)
db.session.add(tc4)
db.session.commit()

# Carga de Coberturas
cob1 = Cobertura(nombre='Mar', id_tipocobertura='1', altura=0)
cob2 = Cobertura(nombre='Río', id_tipocobertura='1', altura=0)
cob3 = Cobertura(nombre='Lago', id_tipocobertura='1', altura=0)
cob4 = Cobertura(nombre='Maíz', id_tipocobertura='2', altura=0)
cob5 = Cobertura(nombre='Soja', id_tipocobertura='2', altura=0)
cob6 = Cobertura(nombre='Girasol', id_tipocobertura='2', altura=0)
cob7 = Cobertura(nombre='Agropiro', id_tipocobertura='2', altura=0)
cob8 = Cobertura(nombre='Alfalfa', id_tipocobertura='2', altura=0)
cob9 = Cobertura(nombre='Cebolla', id_tipocobertura='2', altura=0)
cob10 = Cobertura(nombre='Trigo', id_tipocobertura='2', altura=0)
cob11 = Cobertura(nombre='Zanahoria', id_tipocobertura='2', altura=0)
cob12 = Cobertura(nombre='Barbecho', id_tipocobertura='2', altura=0)
cob13 = Cobertura(nombre='Cebada', id_tipocobertura='2', altura=0)
cob14 = Cobertura(nombre='Rastrojo', id_tipocobertura='2', altura=0)
cob15 = Cobertura(nombre='Suelo', id_tipocobertura='2', altura=0)
cob16 = Cobertura(nombre='Sorgo', id_tipocobertura='2', altura=0)
db.session.add(cob1)
db.session.add(cob2)
db.session.add(cob3)
db.session.add(cob4)
db.session.add(cob5)
db.session.add(cob6)
db.session.add(cob7)
db.session.add(cob8)
db.session.add(cob9)
db.session.add(cob10)
db.session.add(cob11)
db.session.add(cob12)
db.session.add(cob13)
db.session.add(cob14)
db.session.add(cob15)
db.session.add(cob16)
db.session.commit()

# Carga de Instrumento
i1 = Instrumento(codigo='ASDFSPRO',tipo='Espectroradiómetro',instrumento='ASD FieldSpec4-HR',marca='ASD',modelo='FieldSpec 4 Hi-Res',)

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
f = date(2011, 12, 27)
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

l14 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 3, 24)
n = nombre_camp(l14, f)
c14 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'], id_localidad=l14.id)
db.session.add(c14)
db.session.commit()

l15 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 3, 25)
n = nombre_camp(l15, f)
c15 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'], id_localidad=l15.id)
db.session.add(c15)
db.session.commit()

l16 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 4, 24)
n = nombre_camp(l16, f)
c16 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'], id_localidad=l16.id)
db.session.add(c16)
db.session.commit()

l17 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 4, 25)
n = nombre_camp(l17, f)
c17 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'], id_localidad=l17.id)
db.session.add(c17)
db.session.commit()

l18 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 3, 26)
n = nombre_camp(l18, f)
c18 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'], id_localidad=l18.id)
db.session.add(c18)
db.session.commit()

l19 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2012, 10, 18)
n = nombre_camp(l19, f)
c19 = Campania(nombre=n, fecha=f, responsable=['Juan Cobo', 'Guillermo Ibañez', 'Ana Dogliotti',
                                               'Mariana Horlent', 'Claudio Sanchez', 'Carolina Gonzalez'], id_localidad=l19.id)
db.session.add(c19)
db.session.commit()

l20 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2012, 10, 31)
n = nombre_camp(l20, f)
c20 = Campania(nombre=n, fecha=f, responsable=['Juan Cobo', 'Guillermo Ibañez', 'Anabel Lamaro',
                                               'Claudio Sanchez', 'Carolina Gonzalez'], id_localidad=l20.id)
db.session.add(c20)
db.session.commit()

l21 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 1)
n = nombre_camp(l21, f)
c21 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Guillermo Ibañez', 'Anabel Lamaro',
                                                                    'Ana Dogliotti'], id_localidad=l21.id)
db.session.add(c21)
db.session.commit()

l22 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 13)
n = nombre_camp(l22, f)
c22 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Guillermo Ibañez', 'Anabel Lamaro', 'Ana Dogliotti',
                                                                    'Aldana Bini', 'Jesús Pérez'], id_localidad=l22.id)
db.session.add(c22)
db.session.commit()

l23 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 14)
n = nombre_camp(l23, f)
c23 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Anabel Lamaro',
                                                                    'Investigadores belgas'], id_localidad=l23.id)
db.session.add(c23)
db.session.commit()
