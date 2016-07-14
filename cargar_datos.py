#!virtual/bin/python3
# -*- coding: utf-8 -*-
from datetime import date, datetime
from app import db
from app.models import Localidad, Campania, TipoCobertura, Cobertura, Radiometro, Metodologia, Proyecto, Muestra, \
    Fotometro, Gps, Patron, Camara, Punto
from app.utils import nombre_camp, nombre_muestra, nombre_punto

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
cob1 = Cobertura(nombre='MAR', id_tipocobertura=1, altura=0)
cob2 = Cobertura(nombre='RIO', id_tipocobertura=1, altura=0)
cob3 = Cobertura(nombre='LAGO', id_tipocobertura=1, altura=0)
cob4 = Cobertura(nombre='MAIZ', id_tipocobertura=2, altura=0)
cob5 = Cobertura(nombre='SOJA', id_tipocobertura=2, altura=0)
cob6 = Cobertura(nombre='GIRASOL', id_tipocobertura=2, altura=0)
cob7 = Cobertura(nombre='AGROPIRO', id_tipocobertura=2, altura=0)
cob8 = Cobertura(nombre='ALFALFA', id_tipocobertura=2, altura=0)
cob9 = Cobertura(nombre='CEBOLLA', id_tipocobertura=2, altura=0)
cob10 = Cobertura(nombre='TRIGO', id_tipocobertura=2, altura=0)
cob11 = Cobertura(nombre='ZANAHORIA', id_tipocobertura=2, altura=0)
cob12 = Cobertura(nombre='BARBECHO', id_tipocobertura=2, altura=0)
cob13 = Cobertura(nombre='CEBADA', id_tipocobertura=2, altura=0)
cob14 = Cobertura(nombre='RASTROJO', id_tipocobertura=2, altura=0)
cob15 = Cobertura(nombre='SUELO', id_tipocobertura=2, altura=0)
cob16 = Cobertura(nombre='SORGO', id_tipocobertura=2, altura=0)
cob17 = Cobertura(nombre='CEBOLLA-MORADA', id_tipocobertura=2, altura=0)
cob18 = Cobertura(nombre='CALIBRACION', id_tipocobertura=3, altura=0)
cob19 = Cobertura(nombre='LABORATORIO', id_tipocobertura=4, altura=0)
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
db.session.add(cob17)
db.session.add(cob18)
db.session.add(cob19)
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
gps1 = Gps(codigo='GPS', nombre='GPS Garmin', marca='Garmin')
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
met1 = Metodologia(nombre='INTERCALADA',
                 descripcion='Todas las mediciones se hacen en el mismo sitio. Las diferencias entre los puntos son '
                             'temporales, se toma una medicion de esepctralon, luego tres mediciones de agua y cielo '
                             '(intercaladas). Esto se repite tres veces por cada toma o "sitio".',
                 angulo_azimutal=90)
met2 = Metodologia(nombre='MUESTRA-CONTINUA',
                 descripcion='Metodología de toma de muestra continua.',
                 angulo_azimutal=90)
met3 = Metodologia(nombre='AYSA-CLOROFILA-CIANO',
                 descripcion='El balde contenedor se lleno en un 90 % aprox. con liquido. Se hicieron tres réplicas'
                             ' de cada medición (B1,B2,... Bn). Se midió con espetralon una vez para cada set de réplicas',
                 angulo_azimutal=90)
met4 = Metodologia(nombre='LOTE-VARIABILIDAD',
                 descripcion='Se toman puntos de muestreo en todo el lote para captar la variabilidad del mismo. '
                             'En cada punto de muestreo se define una parcela de 5x5 m, en la cual, se tomaron datos '
                             'sistemáticamente. Los datos promediados compondrán la firma espectral del área sensada.',
                 angulo_azimutal=90)
db.session.add(met1)
db.session.add(met2)
db.session.add(met3)
db.session.add(met4)
db.session.commit()

# Carga de Campañas
l1 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2011, 2, 10)
n = nombre_camp(l1, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c1 = Campania(nombre=n, fecha=f, responsables=['Christian Weber', 'Martin Sandoval', 'Anabel Lamaro'],
              id_localidad=l1.id, id_proyecto=p.id)
db.session.add(c1)
db.session.commit()

l2 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 17)
n = nombre_camp(l2, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c2 = Campania(nombre=n, fecha=f, responsables=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero'],
              id_localidad=l2.id, id_proyecto=p.id)
db.session.add(c2)
db.session.commit()

l3 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 18)
n = nombre_camp(l3, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c3 = Campania(nombre=n, fecha=f, responsables=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero'],
              id_localidad=l3.id, id_proyecto=p.id)
db.session.add(c3)
db.session.commit()

l4 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 25)
n = nombre_camp(l4, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c4 = Campania(nombre=n, fecha=f, responsables=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero',
                                              'Maximiliano Pisano'], id_localidad=l4.id, id_proyecto=p.id)
db.session.add(c4)
db.session.commit()

l5 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 2, 26)
n = nombre_camp(l5, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c5 = Campania(nombre=n, fecha=f, responsables=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero',
                                              'Maximiliano Pisano'], id_localidad=l5.id, id_proyecto=p.id)
db.session.add(c5)
db.session.commit()

l6 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2011, 5, 10)
n = nombre_camp(l6, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c6 = Campania(nombre=n, fecha=f, responsables=['Maximiliano Guido', 'Guillermo Ibañez', 'Anabel Lamaro',
                                              'Claudio Sanchez', 'Nicolas Soldati'], id_localidad=l6.id, id_proyecto=p.id)
db.session.add(c6)
db.session.commit()

l7 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2011, 9, 20)
n = nombre_camp(l7, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c7 = Campania(nombre=n, fecha=f, responsables=['Personal de CARU', 'Guillermo Ibañez', 'Josefina Otero'],
              id_localidad=l7.id, id_proyecto=p.id)
db.session.add(c7)
db.session.commit()

l8 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2011, 10, 31)
n = nombre_camp(l8, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c8 = Campania(nombre=n+'-AYSA-CCLORO', fecha=f, responsables=['Juan Cobo', 'Maximiliano Guido', 'Mariana Horlent',
                                                             'Anabel Lamaro', 'Carolina Fernández'], id_localidad=l8.id,
              id_proyecto=p.id)
db.session.add(c8)
db.session.commit()

l9 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2011, 12, 1)
n = nombre_camp(l9, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c9 = Campania(nombre=n+'-AYSA-CCIANO', fecha=f, responsables=['Juan Cobo', 'Maximiliano Guido', 'Mariana Horlent',
                                                             'Anabel Lamaro', 'Carolina Fernández'], id_localidad=l9.id,
              id_proyecto=p.id)
db.session.add(c9)
db.session.commit()

l10 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2011, 12, 1)
n = nombre_camp(l10, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c10 = Campania(nombre=n+'-AYSA-DIATOMEAS', fecha=f, responsables=['Juan Cobo', 'Maximiliano Guido', 'Mariana Horlent',
                                              'Anabel Lamaro', 'Carolina Fernández'], id_localidad=l10.id, id_proyecto=p.id)
db.session.add(c10)
db.session.commit()

l11 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2011, 12, 13)
n = nombre_camp(l11, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c11 = Campania(nombre=n, fecha=f, responsables=['Personal de CARU', 'Guillermo Ibañez', 'Andrea Drozd'],
               id_localidad=l11.id, id_proyecto=p.id)
db.session.add(c11)
db.session.commit()

l12 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2011, 12, 27)
n = nombre_camp(l12, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c12 = Campania(nombre=n, fecha=f, id_localidad=l12.id, id_proyecto=p.id)
db.session.add(c12)
db.session.commit()

l13 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2012, 2, 1)
n = nombre_camp(l13, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c13 = Campania(nombre=n, fecha=f, responsables=['Juan Cobo', 'Nicolás Soldati', 'Claudio Sánchez',
                                                'Carolina Fernández'], id_localidad=l13.id, id_proyecto=p.id)
db.session.add(c13)
db.session.commit()

l14 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 3, 24)
n = nombre_camp(l14, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c14 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'],
               id_localidad=l14.id, id_proyecto=p.id)
db.session.add(c14)
db.session.commit()

l15 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 3, 25)
n = nombre_camp(l15, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c15 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'],
               id_localidad=l15.id, id_proyecto=p.id)
db.session.add(c15)
db.session.commit()

l16 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 4, 24)
n = nombre_camp(l16, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c16 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'],
               id_localidad=l16.id, id_proyecto=p.id)
db.session.add(c16)
db.session.commit()

l17 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 4, 25)
n = nombre_camp(l17, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c17 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'],
               id_localidad=l17.id, id_proyecto=p.id)
db.session.add(c17)
db.session.commit()

l18 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2012, 3, 26)
n = nombre_camp(l18, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c18 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez', 'Andrea Drozd'],
               id_localidad=l18.id, id_proyecto=p.id)
db.session.add(c18)
db.session.commit()

l19 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2012, 10, 18)
n = nombre_camp(l19, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c19 = Campania(nombre=n, fecha=f, responsables=['Juan Cobo', 'Guillermo Ibañez', 'Ana Dogliotti',
                                                'Mariana Horlent', 'Claudio Sanchez', 'Carolina Gonzalez'],
               id_localidad=l19.id, id_proyecto=p.id)
db.session.add(c19)
db.session.commit()

l20 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2012, 10, 31)
n = nombre_camp(l20, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c20 = Campania(nombre=n, fecha=f, responsables=['Juan Cobo', 'Guillermo Ibañez', 'Anabel Lamaro', 'Claudio Sanchez',
                                                'Carolina Gonzalez'], id_localidad=l20.id, id_proyecto=p.id)
db.session.add(c20)
db.session.commit()

l21 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 1)
n = nombre_camp(l21, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c21 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Guillermo Ibañez', 'Anabel Lamaro',
                                                                     'Ana Dogliotti'], id_localidad=l21.id,
               id_proyecto=p.id)
db.session.add(c21)
db.session.commit()

l22 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 13)
n = nombre_camp(l22, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c22 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Guillermo Ibañez', 'Anabel Lamaro',
                                                                     'Ana Dogliotti', 'Aldana Bini', 'Jesús Pérez'],
               id_localidad=l22.id, id_proyecto=p.id)
db.session.add(c22)
db.session.commit()

l23 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 14)
n = nombre_camp(l23, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c23 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Personal de DAyE', 'Ana Dogliotti',
                                                                     'Investigadores belgas'], id_localidad=l23.id,
               id_proyecto=p.id)
db.session.add(c23)
db.session.commit()

l24 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 15)
n = nombre_camp(l24, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c24 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Personal de DAyE', 'Ana Dogliotti',
                                                                     'Investigadores belgas'], id_localidad=l24.id,
               id_proyecto=p.id)
db.session.add(c24)
db.session.commit()

l25 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 16)
n = nombre_camp(l25, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c25 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Personal de DAyE', 'Ana Dogliotti',
                                                                     'Investigadores belgas'], id_localidad=l25.id,
               id_proyecto=p.id)
db.session.add(c25)
db.session.commit()

l26 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 19)
n = nombre_camp(l26, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c26 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l26.id,
               id_proyecto=p.id)
db.session.add(c26)
db.session.commit()

l27 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 21)
n = nombre_camp(l27, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c27 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l27.id,
               id_proyecto=p.id)
db.session.add(c27)
db.session.commit()

l28 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2012, 11, 23)
n = nombre_camp(l28, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c28 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l28.id,
               id_proyecto=p.id)
db.session.add(c28)
db.session.commit()

l29 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 1, 23)
n = nombre_camp(l29, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c29 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Personal de DAyE', 'Ana Dogliotti'],
               id_localidad=l29.id, id_proyecto=p.id)
db.session.add(c29)
db.session.commit()

l30 = Localidad.query.filter_by(nombre='GOLFO SAN MATIAS').first()
f = date(2013, 2, 19)
n = nombre_camp(l30, f)
c30 = Campania(nombre=n, fecha=f, responsables=['Guillermo Ibañez'], id_localidad=l30.id)
db.session.add(c30)
db.session.commit()

l31 = Localidad.query.filter_by(nombre='SAN ANTONIO OESTE').first()
f = date(2013, 2, 20)
n = nombre_camp(l31, f)
c31 = Campania(nombre=n, fecha=f, responsables=['Guillermo Ibañez'], id_localidad=l31.id)
db.session.add(c31)
db.session.commit()

l32 = Localidad.query.filter_by(nombre='LAS GRUTAS').first()
f = date(2013, 2, 21)
n = nombre_camp(l32, f)
c32 = Campania(nombre=n, fecha=f, responsables=['Guillermo Ibañez'], id_localidad=l32.id)
db.session.add(c32)
db.session.commit()

l33 = Localidad.query.filter_by(nombre='PUNTA PIEDRAS').first()
f = date(2013, 2, 27)
n = nombre_camp(l33, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c33 = Campania(nombre=n, fecha=f, responsables=['Guillermo Ibañez', 'Ana Dogliotti', 'Dra. Simionato'],
               id_localidad=l33.id, id_proyecto=p.id)
db.session.add(c33)
db.session.commit()

l34 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 4, 16)
n = nombre_camp(l34, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c34 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Josefina Otero', 'Aldana Bini', 'Ana Dogliotti'],
               id_localidad=l34.id, id_proyecto=p.id)
db.session.add(c34)
db.session.commit()

l35 = Localidad.query.filter_by(nombre='PUNTA PIEDRAS').first()
f = date(2013, 4, 30)
n = nombre_camp(l35, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c35 = Campania(nombre=n, fecha=f, responsables=['Guillermo Ibañez', 'Ana Dogliotti', 'Dra. Simionato'],
               id_localidad=l35.id, id_proyecto=p.id)
db.session.add(c35)
db.session.commit()

l36 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 5, 9)
n = nombre_camp(l36, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c36 = Campania(nombre=n+'-AYSA-CCLORO', fecha=f, responsables=['Juan Cobo', 'Maximiliano Guido', 'Aldana Bini',
                                                               'Anabel Lamaro', 'Carolina Fernandez'],
               id_localidad=l36.id, id_proyecto=p.id)
db.session.add(c36)
db.session.commit()

l37 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2013, 5, 27)
n = nombre_camp(l37, f)
p = Proyecto.query.filter_by(nombre='AYSA-CONAE').first()
c37 = Campania(nombre=n+'-AYSA-CCIANO', fecha=f, responsables=['Juan Cobo', 'Anabel Lamaro', 'Ivanna Tropper'],
               id_localidad=l37.id, id_proyecto=p.id)
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
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c41 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l41.id, id_proyecto=p.id)
db.session.add(c41)
db.session.commit()

l42 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2014, 3, 13)
n = nombre_camp(l42, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c42 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l42.id, id_proyecto=p.id)
db.session.add(c42)
db.session.commit()

l43 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2014, 3, 15)
n = nombre_camp(l43, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c43 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l43.id, id_proyecto=p.id)
db.session.add(c43)
db.session.commit()

l44 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2014, 3, 18)
n = nombre_camp(l44, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c44 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Ivanna Tropper'], id_localidad=l44.id, id_proyecto=p.id)
db.session.add(c44)
db.session.commit()

l45 = Localidad.query.filter_by(nombre='PALERMO').first()
f = date(2014, 4, 15)
n = nombre_camp(l45, f)
p = Proyecto.query.filter_by(nombre='IAFE-CONAE').first()
c45 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsables=['Ivanna Tropper'], id_localidad=l45.id, id_proyecto=p.id)
db.session.add(c45)
db.session.commit()

l46 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2014, 4, 23)
n = nombre_camp(l46, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c46 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l46.id, id_proyecto=p.id)
db.session.add(c46)
db.session.commit()

l47 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2014, 4, 24)
n = nombre_camp(l47, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c47 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l47.id, id_proyecto=p.id)
db.session.add(c47)
db.session.commit()

l48 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2014, 4, 25)
n = nombre_camp(l48, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c48 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l48.id, id_proyecto=p.id)
db.session.add(c48)
db.session.commit()

l49 = Localidad.query.filter_by(nombre='RIO DE LA PLATA').first()
f = date(2014, 5, 1)
n = nombre_camp(l49, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c49 = Campania(nombre=n, fecha=f, responsables=['Ivanna Tropper'], id_localidad=l49.id, id_proyecto=p.id)
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
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c51 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l51.id, id_proyecto=p.id)
db.session.add(c51)
db.session.commit()

l52 = Localidad.query.filter_by(nombre='GUALEGUAYCHU').first()
f = date(2014, 11, 13)
n = nombre_camp(l52, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c52 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l52.id, id_proyecto=p.id)
db.session.add(c52)
db.session.commit()

l53 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2014, 11, 14)
n = nombre_camp(l53, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c53 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l53.id, id_proyecto=p.id)
db.session.add(c53)
db.session.commit()

l54 = Localidad.query.filter_by(nombre='SALTO GRANDE').first()
f = date(2014, 11, 15)
n = nombre_camp(l54, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c54 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l54.id, id_proyecto=p.id)
db.session.add(c54)
db.session.commit()

l55 = Localidad.query.filter_by(nombre='BAHIA SAMBOROMBON').first()
f = date(2014, 11, 22)
n = nombre_camp(l55, f)
c55 = Campania(nombre=n, fecha=f, responsables=['Ivanna Tropper', 'Guillermo Ibañez'], id_localidad=l55.id)
db.session.add(c55)
db.session.commit()

l56 = Localidad.query.filter_by(nombre='HILARIO ASCASUBI').first()
f = date(2014, 12, 15)
n = nombre_camp(l56, f)
p = Proyecto.query.filter_by(nombre='INTA-CONAE').first()
c56 = Campania(nombre=n, fecha=f, responsables=['Alejandro Pezzola', 'Mariana Horlent'], id_localidad=l56.id,
               objetivo='Determinación de la firma espectral de cultivos bajo riego en la zona de Hilario Ascasubi.',
               id_proyecto=p.id)
db.session.add(c56)
db.session.commit()

l57 = Localidad.query.filter_by(nombre='RIO URUGUAY').first()
f = date(2015, 1, 21)
n = nombre_camp(l57, f)
p = Proyecto.query.filter_by(nombre='CARU-CONAE').first()
c57 = Campania(nombre=n, fecha=f, responsables=['Personal CARU', 'Guillermo Ibañez'], id_localidad=l57.id,
               objetivo='Evaluar la contaminacion por algas y sedimentos el cauce del rio Uruguay y la Represa Salto Grande.',
               id_proyecto=p.id)
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
m1 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m1)
db.session.commit()
m2 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m2)
db.session.commit()
m3 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m3)
db.session.commit()
m4 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m4)
db.session.commit()
m5 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m5)
db.session.commit()
m6 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m6)
db.session.commit()
m7 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m7)
db.session.commit()
m8 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Guillermo Ibañez', id_cobertura=cobertura.id, id_campania=campania.id)
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
m9 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m9)
db.session.commit()
cobertura = Cobertura.query.filter_by(nombre='MAIZ').first()
m10 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m10)
db.session.commit()
cobertura = Cobertura.query.filter_by(nombre='GIRASOL').first()
m11 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m11)
db.session.commit()
cobertura = Cobertura.query.filter_by(nombre='ALFALFA').first()
m12 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m12)
db.session.commit()
cobertura = Cobertura.query.filter_by(nombre='CEBOLLA-MORADA').first()
m13 = Muestra(nombre=nombre_muestra(campania, cobertura), id_metodologia=metodologia.id, id_radiometro=radiometro.id,
             id_patron=patron.id, id_camara=camara.id, id_fotometro=fotometro.id, id_gps=gps.id,
             operador='Alejandro Pezzola', id_cobertura=cobertura.id, id_campania=campania.id)
db.session.add(m13)
db.session.commit()


# Carga de Puntos
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M1%')).first()
p1 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 10, 40), altura_medicion=0, presion=1015,
           temperatura=24.8, nubosidad=50, viento_direccion='SO', viento_velocidad=7.5, oleaje='0', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.44279 -33.82656)::geometry', foto='IMG_1140.jpg,IMG_1141.jpg,IMG_1142.jpg')
db.session.add(p1)
db.session.commit()
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M2%')).first()
p2 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 11, 10), altura_medicion=0, presion=1015,
           temperatura=26.69, nubosidad=60, viento_direccion='', viento_velocidad=0, oleaje='0', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.45264 -33.83364)::geometry', foto='IMG_1143.jpg,IMG_1144.jpg,IMG_1145.jpg')
db.session.add(p2)
db.session.commit()
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M3%')).first()
p3 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 12, 0), altura_medicion=0, presion=1015,
           temperatura=26.88, nubosidad=70, viento_direccion='NE', viento_velocidad=2, oleaje='0', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.46019 -33.81852)::geometry', foto='IMG_1146.jpg,IMG_1147.jpg,IMG_1148.jpg')
db.session.add(p3)
db.session.commit()
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M4%')).first()
p4 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 12, 24), altura_medicion=0, presion=1015,
           temperatura=25.31, nubosidad=70, viento_direccion='SO', viento_velocidad=3, oleaje='0', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.44367 -33.78389)::geometry', foto='IMG_1149.jpg,IMG_1150.jpg,IMG_1151.jpg')
db.session.add(p4)
db.session.commit()
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M5%')).first()
p5 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 13, 10), altura_medicion=0, presion=1015,
           temperatura=25.66, nubosidad=20, viento_direccion='SO', viento_velocidad=0, oleaje='0', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.53825 -33.72692)::geometry', foto='IMG_1152.jpg,IMG_1153.jpg,IMG_1154.jpg')
db.session.add(p5)
db.session.commit()
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M6%')).first()
p6 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 13, 40), altura_medicion=0, presion=1015,
           temperatura=25.64, nubosidad=5, viento_direccion='NO', viento_velocidad=3.5, oleaje='5m', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.42336 -33.72503)::geometry', foto='IMG_1155.jpg,IMG_1156.jpg,IMG_1157.jpg')
db.session.add(p6)
db.session.commit()
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M7%')).first()
p7 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 14, 15), altura_medicion=0, presion=1015,
           temperatura=25.8, nubosidad=5, viento_direccion='O', viento_velocidad=8.5, oleaje='5m', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.429 -33.80781)::geometry', foto='IMG_1158.jpg,IMG_1159.jpg,IMG_1160.jpg')
db.session.add(p7)
db.session.commit()
muestra = Muestra.query.filter(Muestra.nombre.like('%20150121-RIOURUGUAY-M8%')).first()
p8 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2015, 1, 21, 14, 45), altura_medicion=0, presion=1015,
           temperatura=26.73, nubosidad=60, viento_direccion='E', viento_velocidad=13, oleaje='10m', id_muestra=muestra.id,
           geom='SRID=4326;POINT(-58.41865 -33.86936)::geometry', foto='IMG_1161.jpg,IMG_1162.jpg,IMG_1163.jpg')
db.session.add(p8)
db.session.commit()


muestra = Muestra.query.filter(Muestra.nombre.like('%20141215-HILARIOASCASUBI-M1%')).first()
p9 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 20), altura_medicion=2, presion=1012,
           nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63305 -39.41874)::geometry',
           foto='90.jpg', observaciones='Tomada a 7m', estado='B')
db.session.add(p9)
db.session.commit()
p10 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 45), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63296 -39.41875)::geometry',
            foto='89.jpg', observaciones='Suelo seco', estado='B', cantidad_tomas=28)
db.session.add(p10)
db.session.commit()
p11 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 48), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.6329 -39.41879)::geometry',
            foto='88.jpg', observaciones='', estado='B', cantidad_tomas=30)
db.session.add(p11)
db.session.commit()
p12 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.6329 -39.41881)::geometry',
            foto='87.jpg', observaciones='Suelo seco', estado='B', cantidad_tomas=34)
db.session.add(p12)
db.session.commit()
p13 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63313 -39.41865)::geometry',
            foto='91.jpg', observaciones='No se midió por pisoteo', estado='B')
db.session.add(p13)
db.session.commit()
p14 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63309 -39.41863)::geometry',
            foto='92.jpg', observaciones='Suelo húmedo', estado='B', cantidad_tomas=26)
db.session.add(p14)
db.session.commit()
p15 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63305 -39.41865)::geometry',
            foto='93.jpg', observaciones='Suelo seco', estado='B', cantidad_tomas=27)
db.session.add(p15)
db.session.commit()
p16 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63302 -39.4187)::geometry',
            foto='94.jpg', observaciones='Suelo intermedio de humedad', estado='B', cantidad_tomas=29)
db.session.add(p16)
db.session.commit()
p17 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=0, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63328 -39.41849)::geometry',
            foto='95.jpg', observaciones='No se midió por pisoteo', estado='B')
db.session.add(p17)
db.session.commit()
p18 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=5, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63325 -39.41848)::geometry',
            foto='96.jpg', observaciones='Bruma en el ambiente', estado='B')
db.session.add(p18)
db.session.commit()
p19 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=5, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63319 -39.41848)::geometry',
            foto='97.jpg', observaciones='Bruma en el ambiente', estado='B')
db.session.add(p19)
db.session.commit()
p20 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 13, 22), altura_medicion=2, presion=1012,
            nubosidad=5, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63317 -39.4185)::geometry',
            foto='98.jpg', observaciones='Bruma en el ambiente', estado='B')
db.session.add(p20)
db.session.commit()
p21 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 14, 10), altura_medicion=2, presion=1012,
            nubosidad=5, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63316 -39.41854)::geometry',
            foto='99.jpg', observaciones='Bruma en el ambiente', estado='B')
db.session.add(p21)
db.session.commit()
p22 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 14, 10), altura_medicion=2, presion=1012,
            nubosidad=5, viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63371 -39.41814)::geometry',
            foto='100.jpg', observaciones='Suelo desnudo', estado='B')
db.session.add(p22)
db.session.commit()
p23 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 14, 10), altura_medicion=2, presion=1012,
            viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63369 -39.41809)::geometry',
            foto='101.jpg', observaciones='En cultivo')
db.session.add(p23)
db.session.commit()
p24 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 14, 10), altura_medicion=2, presion=1012,
            viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63363 -39.41808)::geometry',
            foto='102.jpg', observaciones='Entre surco')
db.session.add(p24)
db.session.commit()
p25 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 14, 10), altura_medicion=2, presion=1012,
            viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63355 -39.41811)::geometry',
            foto='103.jpg', observaciones='')
db.session.add(p25)
db.session.commit()
p26 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 15, 14, 10), altura_medicion=2, presion=1012,
            viento_velocidad=2, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63357 -39.41816)::geometry',
            foto='104.jpg', observaciones='')
db.session.add(p26)
db.session.commit()

muestra = Muestra.query.filter(Muestra.nombre.like('%20141215-HILARIOASCASUBI-M2%')).first()
p27 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 18, 13, 10), altura_medicion=1.8, presion=1005,
            nubosidad=10, viento_velocidad=10, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.60698 -39.30943)::geometry',
            foto='80.jpg,81.jpg', observaciones='Manchón ralo, erosión eólica', estado='B', cantidad_tomas=41)
db.session.add(p27)
db.session.commit()
p28 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 18, 13, 32), altura_medicion=1.8, presion=1005,
            nubosidad=10, viento_velocidad=10, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.606668 -39.30901)::geometry',
            foto='83.jpg,84.jpg', observaciones='Un poco más alto y verde', estado='B', cantidad_tomas=31)
db.session.add(p28)
db.session.commit()
p29 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 18, 13, 44), altura_medicion=1.8, presion=1005,
            nubosidad=10, viento_velocidad=10, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.60579 -39.30783)::geometry',
            foto='86.jpg,87.jpg', observaciones='Un poco más alto y verde', estado='B', cantidad_tomas=32)
db.session.add(p29)
db.session.commit()
p30 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 18, 14, 2), altura_medicion=1.8, presion=1005,
            nubosidad=10, viento_velocidad=10, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.60542 -39.30803)::geometry',
            foto='90.jpg,91.jpg,92.jpg', observaciones='Verde en buen estado', estado='B', cantidad_tomas=31)
db.session.add(p30)
db.session.commit()

muestra = Muestra.query.filter(Muestra.nombre.like('%20141215-HILARIOASCASUBI-M3%')).first()
p31 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 18, 10, 15), altura_medicion=1.8, presion=1008,
            nubosidad=0, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.60875 -39.31826)::geometry',
            foto='55.jpg,56.jpg', observaciones='Altura de plantas 1m, parcela 10x10', estado='B', cantidad_tomas=35)
db.session.add(p31)
db.session.commit()
p32 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 18, 10, 42), altura_medicion=1.8, presion=1008,
            nubosidad=0, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.60888 -39.31853)::geometry',
            foto='58.jpg,59.jpg', observaciones='', estado='B', cantidad_tomas=39)
db.session.add(p32)
db.session.commit()
p33 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 18, 11, 0), altura_medicion=1.8, presion=1008,
            nubosidad=0, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.60359 -39.319)::geometry',
            foto='61.jpg,62.jpg', observaciones='', estado='B', cantidad_tomas=30)
db.session.add(p33)
db.session.commit()

muestra = Muestra.query.filter(Muestra.nombre.like('%20141215-HILARIOASCASUBI-M4%')).first()
p34 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 13, 58), altura_medicion=1.5, presion=1013,
            nubosidad=0, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63107 -39.34538)::geometry',
            foto='', observaciones='', estado='B', cantidad_tomas=5)
db.session.add(p34)
db.session.commit()
p35 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 14, 1), altura_medicion=1.5, presion=1013,
            nubosidad=0, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63071 -39.34531)::geometry',
            foto='', observaciones='', estado='B', cantidad_tomas=5)
db.session.add(p35)
db.session.commit()
p36 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 14, 3), altura_medicion=1.5, presion=1013,
            nubosidad=0, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.6305 -39.34526)::geometry',
            foto='', observaciones='', estado='B', cantidad_tomas=5)
db.session.add(p36)
db.session.commit()

muestra = Muestra.query.filter(Muestra.nombre.like('%20141215-HILARIOASCASUBI-M5%')).first()
p37 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 12, 57), altura_medicion=1.5, presion=1013,
            nubosidad=0, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63227 -39.34511)::geometry',
            foto='15.jpf,16.jpg', observaciones='Cebolla 30 cm', estado='B', cantidad_tomas=30)
db.session.add(p37)
db.session.commit()
p38 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 13, 4), altura_medicion=1.5, presion=1013,
            nubosidad=5, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63259 -39.34522)::geometry',
            foto='19.jpf,20.jpg', observaciones='', estado='B', cantidad_tomas=29)
db.session.add(p38)
db.session.commit()
p39 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 13, 10), altura_medicion=1.5, presion=1013,
            nubosidad=5, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.633 -39.34534)::geometry',
            foto='23.jpf,24.jpg', observaciones='Nubes en el horizonte', estado='B', cantidad_tomas=29)
db.session.add(p39)
db.session.commit()
p40 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 13, 17), altura_medicion=1.5, presion=1013,
            nubosidad=5, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63333 -39.34537)::geometry',
            foto='27.jpf,28.jpg', observaciones='Nubes que vienen', estado='B', cantidad_tomas=29)
db.session.add(p40)
db.session.commit()
p41 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 13, 24), altura_medicion=1.5, presion=1013,
            nubosidad=10, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63294 -39.3457)::geometry',
            foto='31.jpf,32.jpg', observaciones='Nubes que vienen, más pelado', estado='B', cantidad_tomas=29)
db.session.add(p41)
db.session.commit()
p42 = Punto(nombre=nombre_punto(muestra), fecha_hora=datetime(2014, 12, 17, 13, 32), altura_medicion=1.5, presion=1013,
            nubosidad=10, viento_velocidad=3, id_muestra=muestra.id, geom='SRID=4326;POINT(-62.63231 -39.34559)::geometry',
            foto='35.jpf,36.jpg', observaciones='Nubes más arriba', estado='B', cantidad_tomas=29)
db.session.add(p42)
db.session.commit()

