# -*- coding: utf-8 -*-
import fnmatch
import os
from app import db
from app.forms import EditarCampForm, NuevaCampForm, ConsultaCampForm, CoberturaForm, MuestraForm, ConsultarForm
from app.models import Campania, Muestra, Punto, Fotometria, Radiometria, ProductoRadiancia, Proyecto, Localidad, \
    TipoCobertura, Cobertura, Camara, Patron, Radiometro, Gps, Metodologia, Fotometro

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
    camps = Campania.query.filter_by(deleted=False).all()
    ult_id = 0
    l = ''
    # id campaña
    if len(camps) == 0:
        ult_id = '001'
    elif len(camps) < 9:
        ult_id = camps[len(camps) - 1].id + 1
        ult_id = '00' + str(ult_id)
    elif len(camps) < 99:
        ult_id = camps[len(camps) - 1].id + 1
        ult_id = '0' + str(ult_id)
    # fecha
    y = str(f.year)
    m = str(f.month)
    d = str(f.day)
    if f.month < 10:
        m = '0' + str(f.month)
    if f.day < 10:
        d = '0' + str(f.day)
    f = y + m + d
    # localidad
    for c in camps:
        if c.id_localidad == loc.id:
            l = c.nombre.rsplit('-', 1)[1]
            break
    if l is '':
        locs = loc.nombre.split(' ')
        for ls in locs:
            l += ls

    return str(ult_id) + '-' + f + '-' + l


# Crear nombre de la muestra
def nombre_muestra(campania, cobertura):
    m = Muestra.query.filter(Muestra.id_campania == campania.id, Muestra.deleted is False).count()
    ult_id = 0
    if m == 0:
        ult_id = '1'
    if m > 0:
        ult_id = m + 1
    return campania.nombre + '-M' + str(ult_id) + '-' + cobertura.nombre


# Crear nombre del punto
def nombre_punto(muestra):
    p = Punto.query.filter(Punto.id_muestra == muestra.id, Punto.deleted is False).count()
    ult_id = 0
    if p == 0:
        ult_id = '1'
    if p > 0:
        ult_id = p + 1
    return muestra.nombre + '-P' + str(ult_id)


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
def cargar_prod_rad(ur1, ur2, ur3, punto):
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
        form_c = CoberturaForm()
        form_m = MuestraForm()
        view = db.session.query(Campania, Muestra, Cobertura).join(Muestra, Cobertura).\
            filter(Campania.id == id, Campania.deleted is False).all()
        if len(view) > 0:
            camp = view[0][0]
            mues = [view[i][1] for i, v in enumerate(view)]
            cob = [view[i][2] for i, v in enumerate(view)]
            form.campania.data = camp.nombre
            form.proyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.filter_by(deleted=False).order_by('nombre')]
            form.proyecto.data = camp.id_proyecto
            form.localidad.choices = [(l.id, l.nombre) for l in Localidad.query.filter_by(deleted=False).order_by('nombre')]
            form.localidad.data = camp.id_localidad
            form.fecha.data = camp.fecha
            form.responsable.data = camp.responsables
            form.objetivo.data = camp.objetivo
            form_m.metodologia.choices = [(met.id, met.nombre) for met in Metodologia.query.filter_by(deleted=False).order_by('nombre')]
            form_m.metodologia.data = mues[0].id_metodologia
            form_m.fotometro.choices = [(fot.id, fot.nombre) for fot in Fotometro.query.filter_by(deleted=False).order_by('nombre')]
            form_m.fotometro.data = mues[0].id_fotometro
            form_m.camara.choices = [(cam.id, cam.nombre) for cam in Camara.query.filter_by(deleted=False).order_by('nombre')]
            form_m.camara.data = mues[0].id_camara
            form_m.espectralon.choices = [(e.id, e.nombre) for e in Patron.query.filter_by(deleted=False).order_by('nombre')]
            form_m.espectralon.data = mues[0].id_patron
            form_m.radiometro.choices = [(r.id, r.nombre) for r in Radiometro.query.filter_by(deleted=False).order_by('nombre')]
            form_m.radiometro.data = mues[0].id_radiometro
            form_m.gps.choices = [(gps.id, gps.nombre) for gps in Gps.query.filter_by(deleted=False).order_by('nombre')]
            form_m.gps.data = mues[0].id_gps
            form_m.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.filter_by(deleted=False).order_by('nombre')]
            form_m.tipo_cobertura.data = cob[0].id_tipocobertura
            form_c.ecobertura.choices = [(cob.id, cob.nombre) for cob in cob]
            form_c.ecobertura.choices.insert(0, (0, ''))
            form_c.ecobertura_nueva.choices = [(cn.id, cn.nombre) for cn in Cobertura.query.filter_by(deleted=False).order_by('nombre')]
            form_c.ecobertura_nueva.choices.insert(0, (0, ''))
            ult = len(form_c.ecobertura_nueva.choices)
            form_c.ecobertura_nueva.choices.insert(ult, (ult, 'Nueva..'))
            return {'form': form, 'form_c': form_c, 'form_m': form_m}
        if len(view) == 0:
            camp = Campania.query.filter_by(id=id).first()
            form.campania.data = camp.nombre
            form.proyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.filter_by(deleted=False).order_by('nombre')]
            form.proyecto.data = camp.id_proyecto
            form.localidad.choices = [(l.id, l.nombre) for l in Localidad.query.filter_by(deleted=False).order_by('nombre')]
            form.localidad.data = camp.id_localidad
            form.fecha.data = camp.fecha
            form.responsable.data = camp.responsables
            form.objetivo.data = camp.objetivo
            form_m.metodologia.choices = [(met.id, met.nombre) for met in Metodologia.query.filter_by(deleted=False).order_by('nombre')]
            form_m.metodologia.choices.insert(0, (0, ''))
            form_m.fotometro.choices = [(fot.id, fot.nombre) for fot in Fotometro.query.filter_by(deleted=False).order_by('nombre')]
            form_m.fotometro.choices.insert(0, (0, ''))
            form_m.camara.choices = [(cam.id, cam.nombre) for cam in Camara.query.filter_by(deleted=False).order_by('nombre')]
            form_m.camara.choices.insert(0, (0, ''))
            form_m.espectralon.choices = [(e.id, e.nombre) for e in Patron.query.filter_by(deleted=False).order_by('nombre')]
            form_m.espectralon.choices.insert(0, (0, ''))
            form_m.radiometro.choices = [(r.id, r.nombre) for r in Radiometro.query.filter_by(deleted=False).order_by('nombre')]
            form_m.radiometro.choices.insert(0, (0, ''))
            form_m.gps.choices = [(gps.id, gps.nombre) for gps in Gps.query.filter_by(deleted=False).order_by('nombre')]
            form_m.gps.choices.insert(0, (0, ''))
            form_m.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.filter_by(deleted=False).order_by('nombre')]
            form_m.tipo_cobertura.choices.insert(0, (0, ''))
            form_c.ecobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.filter_by(deleted=False).order_by('nombre')]
            form_c.ecobertura.choices.insert(0, (0, ''))
            form_c.ecobertura_nueva.choices = [(cn.id, cn.nombre) for cn in Cobertura.query.filter_by(deleted=False).order_by('nombre')]
            form_c.ecobertura_nueva.choices.insert(0, (0, ''))
            ult = len(form_c.ecobertura_nueva.choices)
            form_c.ecobertura_nueva.choices.insert(ult, (ult, 'Nueva..'))
            return {'form': form, 'form_c': form_c, 'form_m': form_m}
    if id == 0:
        form = EditarCampForm()
        form_c = CoberturaForm()
        form_m = MuestraForm()
        form.proyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.filter_by(deleted=False).order_by('nombre')]
        form.localidad.choices = [(l.id, l.nombre) for l in Localidad.query.filter_by(deleted=False).order_by('nombre')]
        form_m.metodologia.choices = [(met.id, met.nombre) for met in Metodologia.query.filter_by(deleted=False).order_by('nombre')]
        form_m.fotometro.choices = [(fot.id, fot.nombre) for fot in Fotometro.query.filter_by(deleted=False).order_by('nombre')]
        form_m.camara.choices = [(cam.id, cam.nombre) for cam in Camara.query.filter_by(deleted=False).order_by('nombre')]
        form_m.espectralon.choices = [(e.id, e.nombre) for e in Patron.query.filter_by(deleted=False).order_by('nombre')]
        form_m.radiometro.choices = [(r.id, r.nombre) for r in Radiometro.query.filter_by(deleted=False).order_by('nombre')]
        form_m.gps.choices = [(gps.id, gps.nombre) for gps in Gps.query.filter_by(deleted=False).order_by('nombre')]
        form_m.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.filter_by(deleted=False).order_by('nombre')]
        form_c.ecobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.filter_by(deleted=False).order_by('nombre')]
        form_c.ecobertura_nueva.choices = [(cn.id, cn.nombre) for cn in Cobertura.query.filter_by(deleted=False).all()]
        return {'form': form, 'form_c': form_c, 'form_m': form_m}

def ini_actualizar_form(id, idtp):
    form = EditarCampForm()
    form_c = CoberturaForm()
    form_m = MuestraForm()
    camp = Campania.query.filter_by(id=id).first()
    form.campania.data = camp.nombre
    form.proyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.filter_by(deleted=False).order_by('nombre')]
    form.proyecto.data = camp.id_proyecto
    form.localidad.choices = [(l.id, l.nombre) for l in Localidad.query.filter_by(deleted=False).order_by('nombre')]
    form.localidad.data = camp.id_localidad
    form.fecha.data = camp.fecha
    form.responsable.data = camp.responsables
    form.objetivo.data = camp.objetivo
    form_m.camara.choices = [(cam.id, cam.nombre) for cam in Camara.query.filter_by(deleted=False).order_by('nombre')]
    form_m.camara.choices.insert(0, (0, ''))
    form_m.espectralon.choices = [(e.id, e.nombre) for e in Patron.query.filter_by(deleted=False).order_by('nombre')]
    form_m.espectralon.choices.insert(0, (0, ''))
    form_m.radiometro.choices = [(r.id, r.nombre) for r in Radiometro.query.filter_by(deleted=False).order_by('nombre')]
    form_m.radiometro.choices.insert(0, (0, ''))
    form_m.gps.choices = [(gps.id, gps.nombre) for gps in Gps.query.filter_by(deleted=False).order_by('nombre')]
    form_m.gps.choices.insert(0, (0, ''))
    form_m.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.filter_by(deleted=False).order_by('nombre')]
    form_m.tipo_cobertura.choices.insert(0, (0, ''))
    form_c.ecobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.filter_by(deleted=False).order_by('nombre')]
    form_c.ecobertura.choices.insert(0, (0, ''))
    form_c.ecobertura_nueva.choices = [(cn.id, cn.nombre) for cn in
                                       Cobertura.query.filter(Cobertura.id_tipocobertura == idtp).order_by('nombre')]
    form_c.ecobertura_nueva.choices.insert(0, (0, ''))
    ult = len(form_c.ecobertura_nueva.choices)
    form_c.ecobertura_nueva.choices.insert(ult, (ult, 'Nueva..'))
    return {'form': form, 'form_c': form_c, 'form_m': form_m}

def actualizar_tp(idtp):
    form = ConsultarForm()
    form.cobertura.choices = [(cn.id, cn.nombre) for cn in
                              Cobertura.query.filter(Cobertura.id_tipocobertura == idtp).order_by('nombre')]
    form.cobertura.choices.insert(0, (0, ''))
    return form

# Iniciar Formulario Nueva Campaña
def ini_nuevo_form():
    form = NuevaCampForm()
    form.ncampania.data = Campania.query.filter_by(deleted=False).order_by(Campania.id.desc()).first().id + 1
    form.nproyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.filter_by(deleted=False).order_by('nombre')]
    form.nproyecto.choices.insert(0, (0, ''))
    form.nlocalidad.choices = [(l.id, l.nombre) for l in Localidad.query.filter_by(deleted=False).order_by('nombre')]
    form.nlocalidad.choices.insert(0, (0, ''))
    form.ncamara.choices = [(cam.id, cam.nombre) for cam in Camara.query.filter_by(deleted=False).order_by('nombre')]
    form.ncamara.choices.insert(0, (0, ''))
    form.nespectralon.choices = [(e.id, e.nombre) for e in Patron.query.filter_by(deleted=False).order_by('nombre')]
    form.nespectralon.choices.insert(0, (0, ''))
    form.ninstrumento.choices = [(r.id, r.nombre) for r in Radiometro.query.filter_by(deleted=False).order_by('nombre')]
    form.ninstrumento.choices.insert(0, (0, ''))
    form.ngps.choices = [(gps.id, gps.nombre) for gps in Gps.query.filter_by(deleted=False).order_by('nombre')]
    form.ngps.choices.insert(0, (0, ''))
    return form


# Iniciar Formulario Consultar Campaña
def ini_consulta_camp():
    form = ConsultaCampForm()
    form.campania.choices = [(c.id, c.nombre) for c in Campania.query.filter_by(deleted=False).order_by('nombre')]
    form.campania.choices.insert(0, (0, ''))
    return form

# Guardar Campaña Nueva
def camp_nueva(form):
    camp = Campania()
    camp.id_proyecto = form.proyecto.data
    camp.id_localidad = form.localidad.data
    camp.fecha = form.fecha.data
    camp.nombre = nombre_camp(Localidad.query.filter_by(id=camp.id_localidad), camp.fecha)
    camp.responsables = form.responsable.data
    camp.objetivo = form.objetivo.data
    camp.fecha_publicacion = form.fecha_pub.data
    try:
        db.session.add(camp)
        db.commit()
        return camp
    except:
        db.session.rollback()
        return None

# Guardar Campaña Existente
def camp_existente(form, camp):
    camp.nombre = form.campania.data
    camp.id_proyecto = form.proyecto.data
    camp.id_localidad = form.localidad.data
    camp.fecha = form.fecha.data
    camp.responsables = form.responsable.data
    camp.objetivo = form.objetivo.data
    camp.fecha_publicacion = form.fecha_pub.data
    try:
        db.session.add(camp)
        db.commit()
        return camp
    except:
        db.session.rollback()
        return False

# Guardar Muestra Nueva
#######################
# REPLANTEAR LA CARGA DEL FORMULARIO MUESTRA, PARA CONTEMPLAR TODAS LAS MUESTRAS DE UNA CAMPAÑA
#######################
def muestra_nueva(form, camp):
    mues = Muestra()
    cobs = form.cobertura.data.split(',')
    for c in cobs:
        cober = Cobertura.query.filter_by(nombre=c).first()
        mues.nombre = nombre_muestra(camp, cober)
        mues.operador = camp.responsables.split('"')[1]
        mues.id_cobertura = cober.id
        mues.id_campania = camp.id
        mues.id_metodologia = form.metodologia.data
        mues.id_radiometro = form.radiometro.data
        mues.id_camara = form.camara.data
        mues.id_gps = form.gps.data
        mues.id_fotometro = form.fotometro.data
        mues.id_patron = form.espectralon.data
        try:
            db.session.add(mues)
            db.commit()
            return mues
        except:
            db.session.rollback()
            return None

# Guardar Muestra Existente
def muestra_existente(form, camp):
    mues = Muestra.query.join(Campania).filter(Campania.id == camp.id).all()
    cobs = form.cobertura.data.split(',')
    for m in mues:
        m.nombre = m.nombre
        m.operador = camp.responsables.split('"')[1]
        m.id_cobertura = m.id_cobertura
        m.id_campania = camp.id
        m.id_metodologia = form.metodologia.data
        m.id_radiometro = form.radiometro.data
        m.id_camara = form.camara.data
        m.id_gps = form.gps.data
        m.id_fotometro = form.fotometro.data
        m.id_patron = form.espectralon.data
        try:
            db.session.add(m)
            db.commit()
        except:
            db.session.rollback()
            return None

# Guarda Campaña y Muestra
def guardar_camp_mues(form_camp, form_mues):
    camp = Campania.query.filter_by(nombre=form_camp.campania.data).first()
    views = db.session.query(Campania, Muestra, Cobertura).join(Muestra, Cobertura).filter(Campania.id == camp.id).all()
    # Para muestras nuevas
    if len(views) == 0:
        # Campaña nueva
        if camp is None:
            camp = camp_nueva(form_camp)
            if camp is None:
                return False
            campa = Campania.query.filter_by(nombre=camp.nombre).first()
            mues = muestra_nueva(form_mues, campa)
            if mues is None:
                return False
            else:
                return True
        # Campaña existente
        if camp is not None:
            if camp_existente(form_camp, camp) is None:
                return False
            mues = muestra_nueva(form_mues, camp)
            if mues is None:
                return False
            else:
                return True
    if len(views) > 0:
        camp
    return False

# Guarda Campaña sola
def guardar_camp(form):
    camp = Campania.query.filter_by(nombre=form.campania.data).first()
    if camp is None:
        camp = Campania()
        camp.id_proyecto = form.proyecto.data
        camp.id_localidad = form.localidad.data
        camp.fecha = form.fecha.data
        camp.nombre = nombre_camp(Localidad.query.filter_by(id=camp.id_localidad), camp.fecha)
        camp.responsables = form.responsable.data
        camp.objetivo = form.objetivo.data
        camp.fecha_publicacion = form.fecha_pub.data
        try:
            db.session.add(camp)
            db.commit()
            return True
        except:
            db.session.rollback()
            return False
    if camp is not None:
        camp.nombre = form.campania.data
        camp.id_proyecto = form.proyecto.data
        camp.id_localidad = form.localidad.data
        camp.fecha = form.fecha.data
        camp.responsables = form.responsable.data
        camp.objetivo = form.objetivo.data
        camp.fecha_publicacion = form.fecha_pub.data
        try:
            db.session.add(camp)
            db.commit()
            return True
        except:
            db.session.rollback()
            return False

def utf_to_ascii(utf):
    str = utf.encode('utf-8').decode('utf-8').upper()
    d = {'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú', 'U2': 'Ü'}
    if d['A'] in str:
        str = str.replace('Á', 'A')
    if d['E'] in str:
        str = str.replace('É', 'E')
    if d['I'] in str:
        str = str.replace('Í', 'I')
    if d['O'] in str:
        str = str.replace('Ó', 'O')
    if d['U'] in str:
        str = str.replace('Ú', 'U')
    if d['U2'] in str:
        str = str.replace('Ü', 'U')
    return str


def tabular_descargas(descargas):
    descarga = {}
    mes = {'cant': 0, 'mb': 0, 'y': 0, 'mes': 0, 'inst': ''}
    for d in descargas:
        y = d.fecha_descarga.year
        if d.fecha_descarga.year == y and d.fecha_descarga.month == mes['mes'] and d.institucion == 'CONAE.GOV.AR':
            descarga[mes['mes']][0]['mb'] += round(d.tamanio_archivo/1024/1024, 2)
            descarga[mes['mes']][0]['cant'] += 1
        if d.fecha_descarga.year == y and d.fecha_descarga.month != mes['mes'] and d.institucion == 'CONAE.GOV.AR':
            mes = {'cant': 0, 'mb': 0, 'y': 0, 'mes': 0, 'inst': ''}
            arr = []
            mes['mb'] += round(d.tamanio_archivo/1024/1024, 2)
            mes['cant'] += 1
            mes['year'] = y
            mes['inst'] = 'conae'
            mes['mes'] = d.fecha_descarga.month
            arr.append(mes)
            descarga[mes['mes']] = arr
        if d.fecha_descarga.year == y and d.fecha_descarga.month == mes['mes'] and d.institucion != 'CONAE.GOV.AR':
            descarga[mes['mes']][1]['mb'] += round(d.tamanio_archivo/1024/1024, 2)
            descarga[mes['mes']][1]['cant'] += 1
        if d.fecha_descarga.year == y and d.fecha_descarga.month != mes['mes'] and d.institucion != 'CONAE.GOV.AR':
            mes = {'cant': 0, 'mb': 0, 'y': 0, 'mes': 0, 'inst': ''}
            mes['mb'] += round(d.tamanio_archivo/1024/1024, 2)
            mes['cant'] += 1
            mes['year'] = y
            mes['inst'] = 'otros'
            mes['mes'] = d.fecha_descarga.month
            descarga[mes['mes']].append(mes)
    return descarga
