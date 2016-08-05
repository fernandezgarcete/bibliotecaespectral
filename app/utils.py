# -*- coding: utf-8 -*-
import fnmatch
import os
from app import db
from app.forms import EditarCampForm, NuevaCampForm, ConsultaCampForm
from app.models import Campania, Muestra, Punto, Fotometria, Radiometria, ProductoRadiancia, Proyecto, Localidad, \
    TipoCobertura, Cobertura, Camara, Patron, Radiometro, Gps

__author__ = 'Juanjo'
from datetime import datetime

# Cargar archivo de radiancia, reflect, fotos
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
    elif tipo == 'ref1':
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

# Crear nombre de la campaña
def nombre_camp(loc, f):
    camps = Campania.query.all()
    ult_id = 0
    l = ''
    # id campaña
    if len(camps) == 0:
        ult_id = '001'
    elif len(camps) < 9:
        ult_id = camps[len(camps)-1].id + 1
        ult_id = '00'+str(ult_id)
    elif len(camps) < 99:
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

# Crear nombre de la muestra
def nombre_muestra(campania, cobertura):
    m = Muestra.query.filter(Muestra.id_campania == campania.id).count()
    ult_id = 0
    if m == 0:
        ult_id = '1'
    if m > 0:
        ult_id = m + 1
    return campania.nombre+'-M'+str(ult_id)+'-'+cobertura.nombre

# Crear nombre del punto
def nombre_punto(muestra):
    p = Punto.query.filter(Punto.id_muestra == muestra.id).count()
    ult_id = 0
    if p == 0:
        ult_id = '1'
    if p > 0:
        ult_id = p + 1
    return muestra.nombre+'-P'+str(ult_id)

# Buscar archivo
def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# Buscar todos los archivos con el mismo nombre
def find_all_files(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

# Buscar archivos con patron de nombre
def find_pattern_files(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# Carga de archivo Fotometria
def cargar_fotometria(uri, punto):
    f = open(uri, 'r')
    f.readline()
    f.readline()
    for line in f:
        if line != '\n':
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

# Carga de archivo Radiometria
def cargar_radiometria(uri, punto):
    file = open(uri, 'r')
    file.readline()
    for line in file:
        rad = Radiometria()
        ref = line.split('\t')
        rad.longitud_onda = int(ref[0])
        rad.radiancia = float(ref[1].replace(',', '.'))
        rad.id_punto = punto.id
        db.session.add(rad)
        db.session.commit()
    file.close()

# Carga de archivo Reflectancia
def cargar_prod_rad(ur1, ur2, ur3,  punto):
    file1 = open(ur1, 'r')
    file2 = open(ur2, 'r')
    file3 = open(ur3, 'r')
    file1.readline()
    file2.readline()
    file3.readline()
    for line in file1:
        prod = ProductoRadiancia()
        ref = line.split('\t')
        prod.longitud_onda = int(ref[0])
        prod.reflectancia = float(ref[1].replace(',', '.'))
        prod.radiancia_avg = float(file2.readline().split('\t')[1].replace(',', '.'))
        prod.radiancia_std = float(file3.readline().split('\t')[1].replace(',', '.'))
        prod.id_punto = punto.id
        db.session.add(prod)
        db.session.commit()
    file1.close()
    file2.close()
    file3.close()

# Iniciar Formulario Editar Campaña
def ini_editar_form(id):
    if id != 0:
        form = EditarCampForm()
        view = db.session.query(Campania, Muestra, Cobertura).join(Muestra, Cobertura).filter(Campania.id == id).all()
        if len(view) > 0:
            camp = view[0][0]
            mues = [view[i][1] for i, v in enumerate(view)]
            cob = [view[i][2] for i, v in enumerate(view)]
            form.ecampania.data = camp.nombre
            form.eproyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.order_by('nombre')]
            form.eproyecto.data = camp.id_proyecto
            form.elocalidad.choices = [(l.id, l.nombre) for l in Localidad.query.order_by('nombre')]
            form.elocalidad.data = camp.id_localidad
            form.efecha.data = camp.fecha
            form.eresponsable.data = camp.responsables
            form.eobjetivo.data = camp.objetivo
            form.ecamara.choices = [(cam.id, cam.nombre) for cam in Camara.query.order_by('nombre')]
            form.ecamara.data = mues[0].id_camara
            form.eespectralon.choices = [(e.id, e.nombre) for e in Patron.query.order_by('nombre')]
            form.eespectralon.data = mues[0].id_patron
            form.einstrumento.choices = [(r.id, r.nombre) for r in Radiometro.query.order_by('nombre')]
            form.einstrumento.data = mues[0].id_radiometro
            form.egps.choices = [(gps.id, gps.nombre) for gps in Gps.query.order_by('nombre')]
            form.egps.data = mues[0].id_gps
            form.etipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.order_by('nombre')]
            form.etipo_cobertura.data = cob[0].id_tipocobertura
            form.ecobertura.choices = [(cob.id, cob.nombre) for cob in cob]
            form.ecobertura_nueva.choices = [(cn.id, cn.nombre) for cn in Cobertura.query.order_by('nombre')]
            ult = len(form.ecobertura_nueva.choices)
            form.ecobertura_nueva.choices.insert(ult, (ult, 'Nueva..'))
            return form
        if len(view) == 0:
            form = EditarCampForm()
            camp = Campania.query.filter_by(id=id).first()
            form.ecampania.data = camp.nombre
            form.eproyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.order_by('nombre')]
            form.eproyecto.data = camp.id_proyecto
            form.elocalidad.choices = [(l.id, l.nombre) for l in Localidad.query.order_by('nombre')]
            form.elocalidad.data = camp.id_localidad
            form.efecha.data = camp.fecha
            form.eresponsable.data = camp.responsables
            form.eobjetivo.data = camp.objetivo
            form.ecamara.choices = [(cam.id, cam.nombre) for cam in Camara.query.order_by('nombre')]
            form.ecamara.choices.insert(0, (0, ''))
            form.eespectralon.choices = [(e.id, e.nombre) for e in Patron.query.order_by('nombre')]
            form.eespectralon.choices.insert(0, (0, ''))
            form.einstrumento.choices = [(r.id, r.nombre) for r in Radiometro.query.order_by('nombre')]
            form.einstrumento.choices.insert(0, (0, ''))
            form.egps.choices = [(gps.id, gps.nombre) for gps in Gps.query.order_by('nombre')]
            form.egps.choices.insert(0, (0, ''))
            form.etipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.order_by('nombre')]
            form.etipo_cobertura.choices.insert(0, (0, ''))
            form.ecobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.order_by('nombre')]
            form.ecobertura.choices.insert(0, (0, ''))
            form.ecobertura_nueva.choices = [(cn.id, cn.nombre) for cn in Cobertura.query.order_by('nombre')]
            ult = len(form.ecobertura_nueva.choices)
            form.ecobertura_nueva.choices.insert(ult, (ult, 'Nueva..'))
            return form
    if id == 0:
        form = EditarCampForm()
        form.eproyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.order_by('nombre')]
        form.elocalidad.choices = [(l.id, l.nombre) for l in Localidad.query.order_by('nombre')]
        form.ecamara.choices = [(cam.id, cam.nombre) for cam in Camara.query.order_by('nombre')]
        form.eespectralon.choices = [(e.id, e.nombre) for e in Patron.query.order_by('nombre')]
        form.einstrumento.choices = [(r.id, r.nombre) for r in Radiometro.query.order_by('nombre')]
        form.egps.choices = [(gps.id, gps.nombre) for gps in Gps.query.order_by('nombre')]
        form.etipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.order_by('nombre')]
        form.ecobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.order_by('nombre')]
        form.ecobertura_nueva.choices = [(cn.id, cn.nombre) for cn in Cobertura.query.all()]
        return form

# Iniciar Formulario Nueva Campaña
def ini_nuevo_form():
    form = NuevaCampForm()
    form.ncampania.data = Campania.query.order_by(Campania.id.desc()).first().id + 1
    form.nproyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.order_by('nombre')]
    form.nproyecto.choices.insert(0, (0, ''))
    form.nlocalidad.choices = [(l.id, l.nombre) for l in Localidad.query.order_by('nombre')]
    form.nlocalidad.choices.insert(0, (0, ''))
    form.ncamara.choices = [(cam.id, cam.nombre) for cam in Camara.query.order_by('nombre')]
    form.ncamara.choices.insert(0, (0, ''))
    form.nespectralon.choices = [(e.id, e.nombre) for e in Patron.query.order_by('nombre')]
    form.nespectralon.choices.insert(0, (0, ''))
    form.ninstrumento.choices = [(r.id, r.nombre) for r in Radiometro.query.order_by('nombre')]
    form.ninstrumento.choices.insert(0, (0, ''))
    form.ngps.choices = [(gps.id, gps.nombre) for gps in Gps.query.order_by('nombre')]
    form.ngps.choices.insert(0, (0, ''))
    return form

# Iniciar Formulario Consultar Campaña
def ini_consulta_camp():
    form = ConsultaCampForm()
    form.ccampania.choices = [(c.id, c.nombre) for c in Campania.query.order_by('nombre')]
    form.ccampania.choices.insert(0, (0, ''))
    return form
