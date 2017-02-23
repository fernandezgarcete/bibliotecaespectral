# -*- coding: utf-8 -*-
import fnmatch
import json
import os
import time
import zipfile

from app.decorators import async
from app.archivos import guardar_archivo, borrar_datos
from config import UPLOAD_FOLDER, basedir, CAMPAIGNS_FOLDER
from itsdangerous import URLSafeSerializer
import requests
from app import db, app
from app.forms import NuevaCampForm, ConsultaCampForm, CoberturaForm, MuestraForm, ConsultarForm
from app.models import Campania, Muestra, Fotometria, Radiometria, Reflectancia, Proyecto, Localidad, \
    TipoCobertura, Cobertura, Camara, Patron, Radiometro, Gps, Metodologia, Fotometro, RadianciaAvg, ReflectanciaAvg
import geoalchemy2.functions as geofunc

__author__ = 'Juanjo'
from datetime import datetime

# Guardar archivo de radiancia, reflect, fotos
def cargar_archivo(lugar, name, tipo, archivo):
    if tipo == 'rad':
        lugar = os.path.join(lugar, 'rad')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name)
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 1, 'f': file_url}
        except:
            raise
    elif tipo == 'radavg':
        lugar = os.path.join(lugar, 'radavg')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name)
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 2, 'f': file_url}
        except:
            raise
    elif tipo == 'radstd':
        lugar = os.path.join(lugar, 'radstd')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name)
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 3, 'f': file_url}
        except:
            raise
    elif tipo == 'ref1':
        lugar = os.path.join(lugar, 'ref')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name)
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 4, 'f': file_url}
        except:
            raise
    elif tipo == 'refavg':
        lugar = os.path.join(lugar, 'refavg')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name)
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 5, 'f': file_url}
        except:
            raise
    elif tipo == 'refstd':
        lugar = os.path.join(lugar, 'refstd')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name)
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 6, 'f': file_url}
        except:
            raise
    elif tipo == 'img':
        lugar = os.path.join(lugar, 'img')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name.lower())
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 7, 'f': file_url}
        except:
            raise
    elif tipo == 'fot':
        lugar = os.path.join(lugar, 'fot')
        try:
            if not os.path.exists(lugar):
                os.makedirs(lugar)
            file_url = os.path.join(lugar, name)
            archivo.save(file_url)                          # Guarda archivo en disco
            return {'t': 8, 'f': file_url}
        except:
            raise
    else:
        return False


# Guardado asincrono de archivos subidos
@async
def guardar_async(app, paths):
    with app.app_context():
        # Recorrer los paths guardados para leer los archivos y cargar en la base
        for path in paths:
            folders = path.split(os.sep)
            print(datetime.now())
            print('Cargando : %s' % folders[len(folders)-1])
            idp = int(folders[len(folders)-3].split('P')[1])
            guardar_archivo(path, idp)

# Borrar Datos de la Base
# @async
def borrar_async(path, filesnames):
    with app.app_context():
        folders = path.split(os.sep)
        idp = int(folders[len(folders)-2].split('P')[1])
        borrar_datos(path, filesnames, idp)


# Listar directorio si Existe
def list_dir(dir):
    if os.path.exists(dir):
        return os.listdir(dir)


# Zip Comprimir directorio
def zipdir(path, nombre, path_alt=None):
    if path_alt is None:
        path_alt = path
    try:
        zip = zipfile.ZipFile(os.path.join(path_alt, nombre), 'w', zipfile.ZIP_DEFLATED)
        for fname, subf, files in os.walk(path):
            if fname == path:
                name = ''
            else:
                name = os.path.relpath(fname, path)
                zip.write(fname, arcname=name)
            for f in files:
                n = f.rsplit('.')
                if len(n) > 1:
                    if n[1] != 'zip':
                        zip.write(os.path.join(fname, f), arcname=os.path.join(name, f))
        zip.close()
        return True
    except:
        return False

# geom to string
def geom2latlng(list):
    lista = {}
    for l in list:
        x = db.session.scalar(geofunc.ST_X(l.geom))
        y = db.session.scalar(geofunc.ST_Y(l.geom))
        latlng = json.dumps({"lat": x, "lng": y})
        lista[l.id] = latlng
    return lista

# Limpia el campo responsables
def limpia_responsables(str):
    res = str.replace('"', '')
    res1 = res.replace('{', '')
    res2 = res1.replace('}', '')
    return res2

# Averiguar Pagina
def get_page(obj, query, per_page):
    for n in range(1, query.paginate(1, per_page).pages + 1):
        if obj in query.paginate(n, per_page).items:
            return n



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
        prod = Reflectancia()
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

# Valores predeterminado de Punto
def default_punto(form):
    if form.altura.data == '' or form.altura.data == 'None':
        form.altura.data = 0
    if form.temp.data == '' or form.temp.data == 'None':
        form.temp.data = 0
    if form.presion.data == '' or form.presion.data == 'None':
        form.presion.data = 0
    if form.cant_tomas.data == '' or form.cant_tomas.data == 'None':
        form.cant_tomas.data = 0
    if form.nubosidad.data == '' or form.nubosidad.data == 'None':
        form.nubosidad.data = 0
    if form.vel_viento.data == '' or form.vel_viento.data == 'None':
        form.vel_viento.data = 0
    return form

# Iniciar Formulario de Muestras
def ini_muestra_form(id):
    form = MuestraForm()
    view = db.session.query(Campania, Muestra, Cobertura).join(Muestra, Cobertura).\
            filter(Campania.id == id, Campania.deleted is False).all()
    form.campania.data = id
    form.nombre.data = ''
    form.metodologia.choices = [(met.id, met.nombre) for met in Metodologia.query.filter_by(deleted=False).order_by('nombre')]
    form.metodologia.choices.insert(0, (0, ''))
    form.fotometro.choices = [(fot.id, fot.nombre) for fot in Fotometro.query.filter_by(deleted=False).order_by('nombre')]
    form.fotometro.choices.insert(0, (0, ''))
    form.camara.choices = [(cam.id, cam.nombre) for cam in Camara.query.filter_by(deleted=False).order_by('nombre')]
    form.camara.choices.insert(0, (0, ''))
    form.espectralon.choices = [(e.id, e.nombre) for e in Patron.query.filter_by(deleted=False).order_by('nombre')]
    form.espectralon.choices.insert(0, (0, ''))
    form.radiometro.choices = [(r.id, r.nombre) for r in Radiometro.query.filter_by(deleted=False).order_by('nombre')]
    form.radiometro.choices.insert(0, (0, ''))
    form.gps.choices = [(gps.id, gps.nombre) for gps in Gps.query.filter_by(deleted=False).order_by('nombre')]
    form.gps.choices.insert(0, (0, ''))
    form.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.filter_by(deleted=False).order_by('nombre')]
    form.tipo_cobertura.choices.insert(0, (0, ''))
    form.cobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.filter_by(deleted=False).order_by('nombre')]
    form.cobertura.choices.insert(0, (0, ''))
    return form



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
    form.fecha_pub.data = camp.fecha_publicacion
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


# Actualiza las coberturas en base al tipo de cobertura elegido
def actualizar_cob_loc(idtp):
    form = ConsultarForm()
    if idtp > 0:
        form.cobertura.choices = [(cn.id, cn.nombre) for cn in
                                  Cobertura.query.filter(Cobertura.id_tipocobertura == idtp).order_by('nombre')]
        form.localidad.choices = [(loc.id, loc.nombre) for loc in
                                  Localidad.query.join(Campania, Muestra, Cobertura)
                                      .filter(Cobertura.id_tipocobertura == idtp, Campania.fecha_publicacion <= datetime.now())
                                      .order_by('nombre')]
    else:
        form.cobertura.choices = [(cn.id, cn.nombre) for cn in Cobertura.query.order_by('nombre')]
        form.localidad.choices = [(loc.id, loc.nombre) for loc in Localidad.query.order_by('nombre')]
    form.cobertura.choices.insert(0, (0, ''))
    form.localidad.choices.insert(0, (0, ''))
    return form


# Actualiza los tipos coberturas en base a la fuente de datos elegida
def actualizar_tp(idfd):
    form = ConsultarForm()
    if idfd > 0:
        form.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in
                                       TipoCobertura.query.filter(TipoCobertura.id_fuente == idfd).order_by('nombre')]
    else:
        form.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.order_by('nombre')]
    form.tipo_cobertura.choices.insert(0, (0, ''))
    return form


# Iniciar Formulario Nueva Campaña
def ini_nuevo_form():
    form = NuevaCampForm()
    form.id.data = 0
    form.ncampania.data = Campania.query.filter_by(deleted=False).order_by(Campania.id.desc()).first().id + 1
    form.nproyecto.choices = [(pr.id, pr.nombre) for pr in Proyecto.query.filter_by(deleted=False).order_by('nombre')]
    form.nproyecto.choices.insert(0, (0, ''))
    form.nlocalidad.choices = [(l.id, l.nombre) for l in Localidad.query.filter_by(deleted=False).order_by('nombre')]
    form.nlocalidad.choices.insert(0, (0, ''))
    return form


# Iniciar Formulario Consultar Campaña
def ini_consulta_camp():
    choices = [(c.id, c.nombre) for c in Campania.query.filter_by(deleted=False).order_by(Campania.id.desc())]
    form = ConsultaCampForm()
    form.campania.choices = choices
    form.campania.choices.insert(0, (0, ''))
    return form, choices


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
    mes = {'cant': 0, 'mb': 0, 'year': 0, 'mes': 0, 'inst': ''}
    for d in descargas:
        y = d.fecha_descarga.year
        if d.fecha_descarga.year == y and d.fecha_descarga.month == mes['mes']:
            if d.institucion == 'CONAE.GOV.AR':
                descarga[mes['mes']][0]['mb'] += round(d.tamanio_archivo/1024/1024, 2)
                descarga[mes['mes']][0]['cant'] += 1
            else:
                descarga[mes['mes']][1]['mb'] += round(d.tamanio_archivo/1024/1024, 2)
                descarga[mes['mes']][1]['cant'] += 1
        if d.fecha_descarga.year == y and d.fecha_descarga.month != mes['mes']:
            mes = {'cant': 0, 'mb': 0, 'year': 0, 'mes': 0, 'inst': ''}
            arr = []
            if d.institucion == 'CONAE.GOV.AR':
                mes['mb'] += round(d.tamanio_archivo/1024/1024, 2)
                mes['cant'] += 1
                mes['year'] = y
                mes['inst'] = 'conae'
                mes['mes'] = d.fecha_descarga.month
                arr.append(mes)
                descarga[mes['mes']] = arr
                mes = {'cant': 0, 'mb': 0, 'year': y, 'mes': d.fecha_descarga.month, 'inst': 'otros'}
                arr = []
                arr.append(mes)
                descarga[mes['mes']].append(mes)
            else:
                mes = {'cant': 0, 'mb': 0, 'year': y, 'mes': d.fecha_descarga.month, 'inst': 'conae'}
                arr = []
                arr.append(mes)
                descarga[mes['mes']] = arr
                mes = {'cant': 0, 'mb': 0, 'year': y, 'mes': d.fecha_descarga.month, 'inst': 'otros'}
                arr = []
                mes['mb'] += round(d.tamanio_archivo/1024/1024, 2)
                mes['cant'] += 1
                arr.append(mes)
                descarga[mes['mes']].append(mes)
    return descarga

def detalle_archivos(files, path):
    archivos = []
    for f in files:
        archivo = {}
        archivo['nombre'] = f
        archivo['tamanio'] = str(round(os.path.getsize(os.path.join(path, f))/1024/1024, 2)) + ' MB.'
        archivo['fecha'] = datetime.strptime(time.ctime(os.path.getmtime(os.path.join(path, f))),
                                             '%a %b %d %H:%M:%S %Y').date()
        archivos.append(archivo)
    return archivos


# Verificar Robot Captcha
def checkRecaptcha(response, secretkey):
    url = 'https://www.google.com/recaptcha/api/siteverify?'
    url = url + 'secret=' +secretkey
    url = url + '&response=' +response
    try:
        jsonobj = json.loads(requests.get(url).content.decode('utf-8'))
        if jsonobj['success']:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


# Serializar URLs con itsdangerous
def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)


# valores de reflectancia de los puntos
def datos_reflectancia(puntos):
    p = {}                          # Diccionario que contendra puntos individuales y grupales
    cp = 0                          # Contador de puntos
    datos_t = [['Longitud_Onda']]   # Lista de puntos grupales
    for punto in puntos:
        # Recorrido para tomar los datos de cada punto
        datos = []                  # Lista para los datos del punto dado
        # Consulta todos los datos de Reflectancia md del punto
        refs = ReflectanciaAvg.query.filter_by(id_punto=punto.id).order_by('longitud_onda').all()
        cp += 1
        # Si no hay datos para el punto se rellena con 0
        if len(refs) == 0:
            refs = Reflectancia.query.filter_by(id_punto=punto.id).order_by('longitud_onda').all()
        if len(refs) == 0:
            datos = [[0]*2]*2151
        else:
            datos_t[0].append('Punto '+str(cp))       # Agregamos el nombre del punto a la lista grupal
            k = 0                   # Contador de archivos
            j = 0                   # Contador auxiliar para el recorrido de datos por archivos y punto
            d = [0, 0]              # Lista que aloja la Long_Onda y su dato
            # Recorrido que indica cantidad de archivos de rts.md por punto
            for r in refs:
                if r.longitud_onda != refs[0].longitud_onda:
                    break
                k += 1
            # Conociendo la cantidad de archivos, se recorre todos los datos del punto
            for i, r in enumerate(refs):
                # Si hay mas de 1 archivo se rellena haciendo un promedio de todos los datos por archivo para cada WL
                if k > 1:
                    # Condicion para el primer dato
                    if cp == 1 and len(datos_t) == 1:
                        datos_t.append([r.longitud_onda, float(r.reflectancia)])
                    # Condicion cuando el aux sea igual a la cantidad de archivos
                    if j == k:
                        j = 0
                        # Promedio de los datos sobre la cantidad de archivos
                        d[1] = d[1]/k
                        # Se agrega el dato a la lista grupal de datos
                        if i == k:
                            if len(datos_t[0]) == 2:
                                datos_t[1] = list(d)
                            else:
                                datos_t[1].append(d[1])
                        elif len(datos_t[0]) == 2:
                            datos_t.append(list(d))
                        else:
                            datos_t[round(i/k)].append(d[1])
                        # se agrega el dato a la lista de datos del punto
                        datos.append(list(d))
                        d = [0, 0]
                    # Suma de datos en la lista d para posterior promedio
                    d[0] = r.longitud_onda
                    d[1] += float(r.reflectancia)
                    j += 1
                    # Condicion para el último dato del recorrido
                    if i == len(refs)-1:
                        d[1] = d[1]/k
                        if len(datos_t[0]) == 2:
                            datos_t.append(list(d))
                        else:
                            datos_t[round((i+1)/k)].append(d[1])
                        datos.append(list(d))
                        d = [0, 0]
                # Si hay un solo archivo con los datos
                else:
                    d1 = [r.longitud_onda, float(r.reflectancia)]
                    datos.append(list(d1))
                    if cp == 1:
                        datos_t.append(list(d1))
                    else:
                        datos_t[i+1].append(d1[1])
        # Agregamos al diccionario de puntos, al punto con sus datos
        p['Punto '+str(cp)] = list(datos)
    # Al finalizar todos los puntos se agrega el grupo de puntos al diccionario
    p['dt'] = list(datos_t)
    return p


# Valores de reflectancia de las muestras
def detalle_muestra(muestras):
    m = {}
    cm = 0
    datosM = []
    datosM.append(['Longitud_Onda'])
    for m in muestras:
        datosP = []
        datosP.append(['Longitud_Onda'])
        cp = 0
        puntos = m.get_puntos()
        for p in puntos:
            refs = Reflectancia.query.filter_by(id_punto=p.id).order_by('longitud_onda').all()
            cp += 1
            if len(refs) > 0:
                datosP[0].append(m.cobertura_muestra.nombre)
            for i, r in refs:
                if cp < 2:
                    datosP.append([r.longitud_onda, float(r.reflectancia)])
                else:
                    datosP[i+1].append(float(r.reflectancia))
            m[str(p.id)] = datosP
    return m


# Archivos de Reflectancia rts.md
def archivos_reflectancia(puntos):
    archivos = {}
    for i, p in enumerate(puntos):
        ruta = os.path.join('subidas', 'C'+str(p.punto.id_campania))
        ruta = os.path.join(ruta, 'M'+str(p.punto.id))
        ruta = os.path.join(ruta, 'P'+str(p.id))
        ruta_r = os.path.join(ruta, 'ref')
        ruta_ra = os.path.join(ruta, 'refavg')
        ruta_f = os.path.join(ruta, 'img')
        try:
            files = os.listdir(os.path.join(basedir, ruta_r))
            if len(files) > 1:
                if zipdir(os.path.join(basedir, ruta_r), 'reflectancias_punto_'+str(i+1)+'.zip'):
                    for file in os.listdir(os.path.join(basedir, ruta_r)):
                        if file.endswith('.zip'):
                            archivos['P'+str(i+1)] = [ruta_r, file]
            else:
                archivos['P'+str(i+1)] = [ruta_r, files[0]]
        except:
            try:
                files = os.listdir(os.path.join(basedir, ruta_ra))
                if len(files) > 1:
                    if zipdir(os.path.join(basedir, ruta_ra), 'reflectancias_punto_'+str(i+1)+'.zip'):
                        for file in os.listdir(os.path.join(basedir, ruta_ra)):
                            if file.endswith('.zip'):
                                archivos['P'+str(i+1)] = [ruta_ra, file]
                else:
                    archivos['P'+str(i+1)] = [ruta_ra, files[0]]
            except:
                archivos['P'+str(i+1)] = [ruta, '']
        try:
            files_f = os.listdir(os.path.join(basedir, ruta_f))
            if len(files_f) > 0:
                archivos['P'+str(i+1)].append(ruta_f)
                archivos['P'+str(i+1)].append(os.listdir(os.path.join(basedir, ruta_f)))
        except:
            archivos['P'+str(i+1)] = [ruta, '']
    return archivos

