#!virtual/bin/python3
# -*- coding: utf-8 -*-
from datetime import date
from app import db
from app.models import Localidad, Campania, TipoCobertura, Cobertura, Instrumento, Metodologia, Proyecto
from app.utils import nombre_camp

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
i1 = Instrumento(codigo='ASDFS4', tipo='Espectroradiómetro', instrumento='ASD FieldSpec4-HR', marca='ASD',
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
i2 = Instrumento(codigo='ASDFSPRO', tipo='Espectroradiómetro', instrumento='ASD FieldSpec FR', marca='ASD',
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
i3 = Instrumento(codigo='LICOR', tipo='Espectroradiómetro', instrumento='Li-Cor 1800', marca='LICOR',
                 modelo='Li-1800', nro_serie='PRS-199', rango_espectral='300-1100 nm',
                 resolucion_espectral='1 nm', ancho_banda='2 nm', tiempo_escaneo=27, reproducibilidad_ancho_banda=1,
                 exactitud_ancho_banda=1, detector_vnir='300-1100 nm silicon photovoltaic detector',
                 detector_swir1='', detector_swir2='',
                 noice_equivalence_radiance_vnir='350 nm 2x10-7, 400 nm 7x10-8, 500-800 nm 3,5 x10-8, 800-1040 nm 3x10-8',
                 noice_equivalence_radiance_swir1='1100 nm  6x10-8', noice_equivalence_radiance_swir2='',
                 largo_fibra_optica=1.7, fov=3.15, fov_cosenoidal='Receptor cosenoidal  180 º FOV')
i4 = Instrumento(codigo='20788', tipo='Fotómetro', instrumento='Solar Light Microtops II Sunphotometer model 540 - 20788',
                 marca='Solar Light', modelo='Microtops II Sunphotometer model 540 ', nro_serie='20788')
i5 = Instrumento(codigo='17884', tipo='Fotómetro', instrumento='Solar Light Microtops II Sunphotometer model 540 - 17884',
                 marca='Solar Light', modelo='Microtops II Sunphotometer model 540 ', nro_serie='17884')
i6 = Instrumento(codigo='GPS', tipo='GPS', instrumento='GPS Garmin', marca='Garmin')
i7 = Instrumento(codigo='Espectralon', tipo='Patron', instrumento='Patron Espectralon', marca='Spectralon',
                 modelo='Labsphere', nro_serie='2503')
i8 = Instrumento(codigo='Camara', tipo='Camara', instrumento='Canon PowerShot SX700 HS', marca='Canon')
db.session.add(i1)
db.session.add(i2)
db.session.add(i3)
db.session.add(i4)
db.session.add(i5)
db.session.add(i6)
db.session.add(i7)
db.session.commit()

# Carga de Metodologías
m1 = Metodologia(nombre='IAFE-Muelle',
                 descripcion='Todas las mediciones se hicieron en el mismo sitio. Las diferencias entre las puntos son '
                             'temporales, se toma una medicion de esepctralon, luego tres mediciones de agua y cielo '
                             '(intercaladas). Esto se repite tres veces por cada toma o "sitio"',
                 )

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
f = date(2012, 11, 15)
n = nombre_camp(l24, f)
c24 = Campania(nombre=n+'-MUELLE-PESCADORES', fecha=f, responsable=['Personal de DAyE', 'Ana Dogliotti',
                                                                    'Investigadores belgas'], id_localidad=l24.id)
db.session.add(c24)
db.session.commit()