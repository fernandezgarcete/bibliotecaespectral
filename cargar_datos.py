#!virtual/bin/python3
# -*- coding: utf-8 -*-
from datetime import date, datetime
from app import db
from app.models import Localidad, Campania, TipoCobertura, Cobertura, Radiometro, Metodologia, Proyecto, Muestra, \
    Fotometro, Gps, Patron, Camara, Punto
from app.utils import nombre_camp, nombre_muestra

__author__ = 'Juanjo'

# Carga de Proyectos
pro1 = Proyecto(nombre='CARU-CONAE')
pro2 = Proyecto(nombre='AYSA-CONAE')
pro3 = Proyecto(nombre='IAFE-CONAE')
pro4 = Proyecto(nombre='INTA-CONAE')
pro5 = Proyecto(nombre='CETT-CONAE')
pro6 = Proyecto(nombre='INVAP-CONAE')
pro7 = Proyecto(nombre='INIDEP-CONAE')
db.session.add(pro1)
db.session.add(pro2)
db.session.add(pro3)
db.session.add(pro4)
db.session.add(pro5)
db.session.add(pro6)
db.session.add(pro7)
db.session.commit()

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
cob1 = Cobertura(nombre='MAR', id_tipocobertura='1', altura=0)
cob2 = Cobertura(nombre='RIO', id_tipocobertura='1', altura=0)
cob3 = Cobertura(nombre='LAGO', id_tipocobertura='1', altura=0)
cob4 = Cobertura(nombre='MAIZ', id_tipocobertura='2', altura=0)
cob5 = Cobertura(nombre='SOJA', id_tipocobertura='2', altura=0)
cob6 = Cobertura(nombre='GIRASOL', id_tipocobertura='2', altura=0)
cob7 = Cobertura(nombre='AGROPIRO', id_tipocobertura='2', altura=0)
cob8 = Cobertura(nombre='ALFALFA', id_tipocobertura='2', altura=0)
cob9 = Cobertura(nombre='CEBOLLA', id_tipocobertura='2', altura=0)
cob10 = Cobertura(nombre='TRIGO', id_tipocobertura='2', altura=0)
cob11 = Cobertura(nombre='ZANAHORIA', id_tipocobertura='2', altura=0)
cob12 = Cobertura(nombre='BARBECHO', id_tipocobertura='2', altura=0)
cob13 = Cobertura(nombre='CEBADA', id_tipocobertura='2', altura=0)
cob14 = Cobertura(nombre='RASTROJO', id_tipocobertura='2', altura=0)
cob15 = Cobertura(nombre='SUELO', id_tipocobertura='2', altura=0)
cob16 = Cobertura(nombre='SORGO', id_tipocobertura='2', altura=0)
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

# Carga de Instrumentos
r1 = Radiometro(codigo='ASDFS4', nombre='ASD FieldSpec4-HR', marca='ASD',
                 modelo='FieldSpec 4 Hi-Res', nro_serie='18285', rango_espectral='350-2500 nm',
                 resolucion_espectral='3 nm @ 700 nm - 8nm @ 1400/2100 nm',
                 ancho_banda='1.4 nm @ 350-1000 nm - 1.1 nm @ 1001-2500 nm',
                 tiempo_escaneo=0.00100, reproducibilidad_ancho_banda=0.1, exactitud_ancho_banda=0.5,
                 detector_vnir='VNIR detector (350-1000 nm): 512 element silicon array',
                 detector_swir1='SWIR 1 detector (1001-1800 nm): Graded Index InGaAs Photodiode, Two Stage TE Cooled',
                 detector_swir2='SWIR 2 detector (1801-2500 nm): Graded Index InGaAs Photodiode, Two Stage TE Cooled',
                 noice_equivalence_radiance_vnir='VNIR  1.0 X10-9  W/cm2/nm/sr @700 nm',
                 noice_equivalence_radiance_swir1='SWIR 1  1.4 X10-9  W/cm2/nm/sr @ 1400 nm',
                 noice_equivalence_radiance_swir2='SWIR 2  2.2 X10-9  W/cm2/nm/sr @ 2100 nm',
                 largo_fibra_optica=1.5, fov=25, fov_cosenoidal='')
r2 = Radiometro(codigo='ASDFSPRO', nombre='ASD FieldSpec FR', marca='ASD',
                 modelo='FieldSpec Pro FR', nro_serie='6250', rango_espectral='350-2500 nm',
                 resolucion_espectral='3 nm @ 700 nm - 10nm @ 1400/2100 nm',
                 ancho_banda='1.4 nm @ 350-1000 nm - 2 nm @ 1001-2500 nm',
                 tiempo_escaneo=0.1, reproducibilidad_ancho_banda=0.3, exactitud_ancho_banda=1,
                 detector_vnir='VNIR detector (350-1000 nm): 512 element silicon array',
                 detector_swir1='SWIR 1 detector (1001-1800 nm): Graded Index InGaAs Photodiode, Two Stage TE Cooled',
                 detector_swir2='SWIR 2 detector (1801-2500 nm): Graded Index InGaAs Photodiode, Two Stage TE Cooled',
                 noice_equivalence_radiance_vnir='VNIR  1.0 X10-9  W/cm2/nm/sr @700 nm',
                 noice_equivalence_radiance_swir1='SWIR 1  1.4 X10-9  W/cm2/nm/sr @ 1400 nm',
                 noice_equivalence_radiance_swir2='SWIR 2  2.2 X10-9  W/cm2/nm/sr @ 2100 nm',
                 largo_fibra_optica=1.5, fov=25, fov_cosenoidal='Receptor cosenoidal (RCR) 180 º FOV')
r3 = Radiometro(codigo='LICOR', nombre='Li-Cor 1800', marca='LICOR',
                 modelo='Li-1800', nro_serie='PRS-199', rango_espectral='300-1100 nm',
                 resolucion_espectral='1 nm', ancho_banda='2 nm', tiempo_escaneo=27, reproducibilidad_ancho_banda=1,
                 exactitud_ancho_banda=1, detector_vnir='300-1100 nm silicon photovoltaic detector',
                 detector_swir1='', detector_swir2='',
                 noice_equivalence_radiance_vnir='350 nm 2x10-7, 400 nm 7x10-8, 500-800 nm 3,5 x10-8, 800-1040 nm 3x10-8',
                 noice_equivalence_radiance_swir1='1100 nm  6x10-8', noice_equivalence_radiance_swir2='',
                 largo_fibra_optica=1.7, fov=3.15, fov_cosenoidal='Receptor cosenoidal  180 º FOV')
fot1 = Fotometro(codigo='FOT20788', nombre='Solar Light Microtops II Sunphotometer model 540 - 20788',
                 marca='Solar Light', modelo='Microtops II Sunphotometer model 540 ', nro_serie='20788')
fot2 = Fotometro(codigo='FOT17884', nombre='Solar Light Microtops II Sunphotometer model 540 - 17884',
                 marca='Solar Light', modelo='Microtops II Sunphotometer model 540 ', nro_serie='17884')
gps1 = Gps(codigo='GPS', tipo='GPS', instrumento='GPS Garmin', marca='Garmin')
pat1 = Patron(codigo='ESPECTRALON', nombre='Espectralon', marca='Spectralon',
                 modelo='LABSPHERE', nro_serie='2503')
cam1 = Camara(codigo='CAMARA', nombre='Canon PowerShot SX700 HS', marca='Canon')
db.session.add(r1)
db.session.add(r2)
db.session.add(r3)
db.session.add(fot1)
db.session.add(fot2)
db.session.add(gps1)
db.session.add(pat1)
db.session.add(cam1)
db.session.commit()

# Carga de Metodologías
m1 = Metodologia(nombre='INTERCALADA',
                 descripcion='Todas las mediciones se hacen en el mismo sitio. Las diferencias entre los puntos son '
                             'temporales, se toma una medicion de esepctralon, luego tres mediciones de agua y cielo '
                             '(intercaladas). Esto se repite tres veces por cada toma o "sitio".',
                 angulo_azimutal=90)
m2 = Metodologia(nombre='MUESTRA-CONTINUA',
                 descripcion='Metodología de toma de muestra continua.',
                 angulo_azimutal=90)
m3 = Metodologia(nombre='AYSA-CLOROFILA-CIANO',
                 descripcion='El balde contenedor se lleno en un 90 % aprox. con liquido. Se hicieron tres réplicas'
                             ' de cada medición (B1,B2,... Bn). Se midió con espetralon una vez para cada set de réplicas',
                 angulo_azimutal=90)
m4 = Metodologia(nombre='LOTE-VARIABILIDAD',
                 descripcion='Se toman puntos de muestreo en todo el lote para captar la variabilidad del mismo. '
                             'En cada punto de muestreo se define una parcela de 5x5 m, en la cual, se tomaron datos '
                             'sistemáticamente. Los datos promediados compondrán la firma espectral del área sensada.',
                 angulo_azimutal=90)
db.session.add(m1)
db.session.add(m2)
db.session.add(m3)
db.session.add(m4)
db.session.commit()

# Carga de Campañas
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
c23 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l23.id)
db.session.add(c23)
db.session.commit()

l24 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 15)
n = nombre_camp(l24, f)
c24 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l24.id)
db.session.add(c24)
db.session.commit()

l25 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 16)
n = nombre_camp(l25, f)
c25 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l25.id)
db.session.add(c25)
db.session.commit()

l26 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 19)
n = nombre_camp(l26, f)
c26 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l26.id)
db.session.add(c26)
db.session.commit()

l27 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 21)
n = nombre_camp(l27, f)
c27 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l27.id)
db.session.add(c27)
db.session.commit()

l28 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 23)
n = nombre_camp(l28, f)
c28 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l28.id)
db.session.add(c28)
db.session.commit()

l29 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 1, 23)
n = nombre_camp(l29, f)
c29 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti'],
               id_localidad=l29.id)
db.session.add(c29)
db.session.commit()

l30 = Localidad.query.filter_by(nombre='GOLFO SAN MATIAS').first()
f = date(2013, 2, 19)
n = nombre_camp(l30, f)
c30 = Campania(nombre=n, fecha=f, responsable=['Guillermo Ibañez'], id_localidad=l30.id)
db.session.add(c30)
db.session.commit()

l31 = Localidad.query.filter_by(nombre='SAN ANOTNIO OESTE').first()
f = date(2013, 2, 20)
n = nombre_camp(l31, f)
c31 = Campania(nombre=n, fecha=f, responsable=['Guillermo Ibañez'], id_localidad=l31.id)
db.session.add(c31)
db.session.commit()

l32 = Localidad.query.filter_by(nombre='LAS GRUTAS').first()
f = date(2013, 2, 21)
n = nombre_camp(l32, f)
c32 = Campania(nombre=n, fecha=f, responsable=['Guillermo Ibañez'], id_localidad=l32.id)
db.session.add(c32)
db.session.commit()

l33 = Localidad.query.filter_by(nombre='PUNTA PIEDRAS').first()
f = date(2013, 2, 27)
n = nombre_camp(l33, f)
c33 = Campania(nombre=n, fecha=f, responsable=['Guillermo Ibañez', 'Ana Dogliotti', 'Dra. Simionato'], id_localidad=l33.id)
db.session.add(c33)
db.session.commit()

l34 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 4, 16)
n = nombre_camp(l34, f)
c34 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Josefina Otero', 'Aldana Bini', 'Ana Dogliotti'],
               id_localidad=l34.id)
db.session.add(c34)
db.session.commit()

l35 = Localidad.query.filter_by(nombre='PUNTA PIEDRAS').first()
f = date(2013, 4, 30)
n = nombre_camp(l35, f)
c35 = Campania(nombre=n, fecha=f, responsable=['Guillermo Ibañez', 'Ana Dogliotti', 'Dra. Simionato'], id_localidad=l35.id)
db.session.add(c35)
db.session.commit()

l36 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 5, 9)
n = nombre_camp(l36, f)
c36 = Campania(nombre=n+'-AYSA-CCLORO', fecha=f, responsable=['Juan Cobo', 'Maximiliano Guido', 'Aldana Bini',
                                                              'Anabel Lamaro', 'Carolina Fernandez'], id_localidad=l36.id)
db.session.add(c36)
db.session.commit()

l37 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 5, 27)
n = nombre_camp(l37, f)
c37 = Campania(nombre=n+'-AYSA-CCIANO', fecha=f, responsable=['Juan Cobo', 'Anabel Lamaro', 'Ivanna Tropper'],
               id_localidad=l37.id)
db.session.add(c37)
db.session.commit()

l38 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2013, 11, 20)
n = nombre_camp(l38, f)
c38 = Campania(nombre=n, fecha=f, id_localidad=l38.id)
db.session.add(c38)
db.session.commit()

l39 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2013, 12, 20)
n = nombre_camp(l39, f)
c39 = Campania(nombre=n, fecha=f, id_localidad=l39.id)
db.session.add(c39)
db.session.commit()

l40 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2014, 1, 6)
n = nombre_camp(l40, f)
c40 = Campania(nombre=n, fecha=f, id_localidad=l40.id)
db.session.add(c40)
db.session.commit()

l41 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2014, 3, 12)
n = nombre_camp(l41, f)
c41 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l41.id)
db.session.add(c41)
db.session.commit()

l42 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2014, 3, 13)
n = nombre_camp(l42, f)
c42 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l42.id)
db.session.add(c42)
db.session.commit()

l43 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2014, 3, 15)
n = nombre_camp(l43, f)
c43 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l43.id)
db.session.add(c43)
db.session.commit()

l44 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2014, 3, 18)
n = nombre_camp(l44, f)
c44 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Ivanna Tropper'], id_localidad=l44.id)
db.session.add(c44)
db.session.commit()

l45 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2014, 4, 15)
n = nombre_camp(l45, f)
c45 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Ivanna Tropper'], id_localidad=l45.id)
db.session.add(c45)
db.session.commit()

l46 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2014, 4, 23)
n = nombre_camp(l46, f)
c46 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l46.id)
db.session.add(c46)
db.session.commit()

l47 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2014, 4, 24)
n = nombre_camp(l47, f)
c47 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l47.id)
db.session.add(c47)
db.session.commit()

l48 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2014, 4, 25)
n = nombre_camp(l48, f)
c48 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l48.id)
db.session.add(c48)
db.session.commit()

l49 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2014, 5, 1)
n = nombre_camp(l49, f)
c49 = Campania(nombre=n, fecha=f, responsable=['Ivanna Tropper'], id_localidad=l49.id)
db.session.add(c49)
db.session.commit()

l50 = Localidad.query.filter_by(nombre='FALDA DEL CARMEN').first()
f = date(2014, 5, 7)
n = nombre_camp(l50, f)
c50 = Campania(nombre=n, fecha=f, id_localidad=l50.id)
db.session.add(c50)
db.session.commit()

l51 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2014, 11, 12)
n = nombre_camp(l51, f)
c51 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l51.id)
db.session.add(c51)
db.session.commit()

l52 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2014, 11, 13)
n = nombre_camp(l52, f)
c52 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l52.id)
db.session.add(c52)
db.session.commit()

l53 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2014, 11, 14)
n = nombre_camp(l53, f)
c53 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l53.id)
db.session.add(c53)
db.session.commit()

l54 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2014, 11, 15)
n = nombre_camp(l54, f)
c54 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l54.id)
db.session.add(c54)
db.session.commit()

l55 = Localidad.query.filter_by(nombre='BAHIA SAMBOROMBON').first()
f = date(2014, 11, 22)
n = nombre_camp(l55, f)
c55 = Campania(nombre=n, fecha=f, responsable=['Ivanna Tropper', 'Guillermo Ibañez'], id_localidad=l55.id)
db.session.add(c55)
db.session.commit()

l56 = Localidad.query.filter_by(nombre='HILARIO ASCASUBI').first()
f = date(2014, 12, 15)
n = nombre_camp(l56, f)
c56 = Campania(nombre=n, fecha=f, responsable=['Alejandro Pezzola', 'Mariana Horlent'], id_localidad=l56.id,
               objetivo='Determinación de la firma espectral de cultivos bajo riego en la zona de Hilario Ascasubi.',
               id_proyecto=Proyecto.query.filter_by(nombre='INTA-CONAE').first().id)
db.session.add(c56)
db.session.commit()

l57 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2015, 1, 21)
n = nombre_camp(l57, f)
c57 = Campania(nombre=n, fecha=f, responsable=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l57.id,
               objetivo='Evaluar la contaminacion por algas y sedimentos el cauce del rio Uruguay y la Represa Salto Grande.',
               id_proyecto=Proyecto.query.filter_by(nombre='CARU-CONAE').first().id)
db.session.add(c57)
db.session.commit()

# Carga de Muestras
campania = Campania.query.filter(Campania.nombre.like('%20150121-RIOURUGUAY')).first()
metodologia = Metodologia.query.filter_by(nombre='INTERCALADA').first()
radiometro = Radiometro.query.filter_by(codigo='ASDFSPRO').first()
patron = Patron.query.filter_by(codigo='ESPECTRALON').first()
camara = Camara.query.filter_by(codigo='CAMARA').first()
fotometro = Fotometro.query.filter_by(codigo='FOT17884').first()
gps = Gps.query.filter_by(codigo='GPS').first()
cobertura = Cobertura.query.filter_by(nombre='RIO').first()
m1 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
m2 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
m3 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
m4 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
m5 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
m6 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
m7 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
m8 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m1)
db.session.add(m2)
db.session.add(m3)
db.session.add(m4)
db.session.add(m5)
db.session.add(m6)
db.session.add(m7)
db.session.add(m8)
db.session.commit()

campania = Campania.query.filter(Campania.nombre.like('%20141215-HILARIOASCASUBI')).first()
metodologia = Metodologia.query.filter_by(nombre='LOTE-VARIABILIDAD').first()
radiometro = Radiometro.query.filter_by(codigo='ASDFSPRO').first()
patron = Patron.query.filter_by(codigo='ESPECTRALON').first()
camara = Camara.query.filter_by(codigo='CAMARA').first()
fotometro = Fotometro.query.filter_by(codigo='FOT17884').first()
gps = Gps.query.filter_by(codigo='GPS').first()
cobertura = Cobertura.query.filter_by(nombre='CEBOLLA').first()
m9 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
m10 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
m11 = Muestra(nombre=nombre_muestra(campania), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m9)
db.session.add(m10)
db.session.add(m11)
db.session.commit()

# Carga de Puntos
p1 = Punto(nombre='P1', fecha_hora=datetime(2014,1,21,10,40), geom='{POINT(-33,82656 -58,44279), SRID=4326}',
           altura_medicion=0, presion=1015, temperatura=24.8, nubosidad=50, viento_direccion='SO',
           viento_velocidad=7.5, oleaje='0', obsevaciones='', foto='IMG_1140.jpg,IMG_1141.jpg,IMG_1142.jpg',
           id_muestra=Muestra.query.filter())

