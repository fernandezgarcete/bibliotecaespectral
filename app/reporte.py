# -*- coding: utf-8 -*-
import json
import os
import glob
from app.utils import geom2latlng

__author__ = 'Juanjo'

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from config import basedir, UPLOAD_FOLDER


# Genera un resumen de la Campaña con sus Datos
def reporte_campania(camp):
    pdfdir = os.path.join(UPLOAD_FOLDER, 'C' + str(camp.id))
    doc = SimpleDocTemplate(os.path.join(pdfdir, camp.nombre+'.pdf'), rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    elements = []
    dir = os.path.join(basedir, 'app')
    dir = os.path.join(dir, 'static')
    dir = os.path.join(dir, 'img')
    logo = os.path.join(dir, 'CONAE_chico_transp.png')
    img = Image(logo, 2*inch, 1.5*inch)

    elements.append(img)
    elements.append(Spacer(1, 12))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    ptxt = '<font size=18>Biblioteca Nacional de Firmas Espectrales</font>'
    elements.append(Paragraph(ptxt, styles['Center']))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))

    ptxt = '<font size=18>Campaña</font>'
    elements.append(Paragraph(ptxt, styles['Normal']))
    elements.append(Spacer(1, 12))

    muestras = camp.get_muestras()
    puntos = dict()
    cobs = ''
    tp = ''
    esp = ''
    if len(muestras) > 0:
        tp = muestras[0].cobertura_muestra.cobertura.nombre
        esp = muestras[0].patron_muestra.nombre
        for i, m in enumerate(muestras):
            puntos[m.id] = m.get_puntos()
            if i == len(muestras)-1:
                cobs += m.cobertura_muestra.nombre
            else:
                cobs += m.cobertura_muestra.nombre + ', '

    rawdata = [['<b>Nombre</b>', camp.nombre],
               ['<b>Objetivo</b>', camp.objetivo],
               ['<b>Tipo de Cobertura</b>', tp],
               ['<b>Cobertura/s</b>', cobs],
               ['<b>Ubicación</b>', camp.localidad_campania.nombre],
               ['<b>Tipo de Calibración</b>', esp],
               ['<b>Fecha</b>', str(camp.fecha.date())],
               ['<b>Responsables</b>', camp.responsables]]

    table = style_camp(rawdata, styles)
    elements.append(table)

    if muestras:
        for m in muestras:
            elements.append(Spacer(1, 12))
            ptxt = '<font size=16>Muestra</font>'
            elements.append(Paragraph(ptxt, styles['Normal']))
            elements.append(Spacer(1, 12))
            data_muestra = raw_muestra(m)
            tabla_muestra = style_muestra(data_muestra, styles)
            elements.append(tabla_muestra)
            elements.append(Spacer(1, 12))

            if puntos[m.id]:
                ptxt = '<font size=16>Puntos</font>'
                elements.append(Paragraph(ptxt, styles['Normal']))
                elements.append(Spacer(1, 12))
                latlngs = geom2latlng(puntos[m.id])
                for p in puntos[m.id]:
                    data_punto = raw_punto(p, latlngs)
                    tabla_punto = style_punto(data_punto, styles)
                    elements.append(tabla_punto)
                    elements.append(Spacer(1, 12))
                    tabla_fotos = [incluir_fotos(p)]
                    elements.append(Table(tabla_fotos)) if tabla_fotos[0] else ''
                    elements.append(Spacer(1, 12))

    # Al terminar de agregar los elementos se crea el documento
    doc.build(elements)
    return True


# Retorna el conjunto de muestras
def raw_muestra(muestra):
    rawmuestra = [['<b>Muestra</b>', muestra.cobertura_muestra.nombre],
                  ['<b>Proyecto</b>', muestra.campania_muestra.proyecto_campania.nombre],
                  ['<b>Pregunta de Teledectección</b>', muestra.campania_muestra.teledeteccion if muestra.campania_muestra.teledeteccion else '-'],
                  ['<b>Pregunta de Especialidad</b>', muestra.campania_muestra.especialidad if muestra.campania_muestra.especialidad else '-'],
                  ['<b>Espectro-radiómetro</b>', muestra.radiometro_muestra.nombre],
                  ['<b>Otros Instrumentos</b>', '<b>FOTOMETRO:</b> '+muestra.fotometro_muestra.nombre +
                   ', \n<b>CAMARA:</b> '+muestra.camara_muestra.nombre+', \n<b>GPS:</b> '+muestra.gps_muestra.nombre +
                   ', \n<b>PATRON:</b> '+muestra.patron_muestra.nombre],
                  ['<b>Metodología</b>', muestra.metodo_muestra.nombre],
                  ['<b>Puntos</b>', str(len(muestra.get_puntos()))]]
    return rawmuestra


# Retorna el conjunto de muestras
def raw_punto(punto, latlngs):
    latlng = json.loads(latlngs[punto.id])
    e = {'M': 'Malo', 'A': 'Aceptable', 'B': 'Bueno', 'MB': 'Muy Bueno', 'E': 'Excelente'}
    rawpunto = [['<b>Punto</b>', 'P'+str(punto.id)],
                ['<b>Hora</b>', str(punto.fecha_hora.timetz()) + ' ART'],
                ['<b>Ubicación</b>', 'Latitud: '+str(latlng['lat']) + ' \nLongitud: '+str(latlng['lng'])],
                ['<b>Nubosidad</b>', str(punto.nubosidad) + ' %' if punto.nubosidad else '-'],
                ['<b>Estado</b>', e[punto.estado] if punto.estado in e else '-'],
                ['<b>Observaciones</b>', punto.observaciones if punto.observaciones else '-']]
    return rawpunto


# Retorna las foto del Punto
def incluir_fotos(punto):
    fdir = os.path.join(UPLOAD_FOLDER, 'C'+str(punto.punto.campania_muestra.id))
    fdir = os.path.join(fdir, 'M'+str(punto.punto.id))
    fdir = os.path.join(fdir, 'P'+str(punto.id))
    fdir = os.path.join(fdir, 'img')
    for f in punto.foto.split(','):
        if f and f != '':
            thumbnails(os.path.join(fdir, f))
    fotos = [Image(f, 1*inch, 1*inch) if f != '' else ' ' for f in glob.glob(fdir + '/*.thumb*')]
    return fotos


# Crear Vistas previas
def thumbnails(path):
    from PIL import Image
    size = 384, 384
    for infile in glob.glob(path):
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        im.thumbnail(size)
        im.save(file + '.thumb', 'JPEG')


# Retorna la tabla Campania con su estilo
def style_camp(rawcamp, styles):
    tstyle = TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                         ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.lightgrey),
                         ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
    s = styles['BodyText']
    s.wordWrap = 'CJK'
    data = [[Paragraph(cell, s) for cell in row] for row in rawcamp]
    table = Table(data)
    table.setStyle(tstyle)
    return table


# Retorna tabla de Muestra con su estilo
def style_muestra(rawmuestra, styles):
    tstyle = TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                         ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.lightgrey),
                         ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
    s = styles['BodyText']
    s.wordWrap = 'CJK'
    data = [[Paragraph(cell, s) for cell in row] for row in rawmuestra]
    table = Table(data)
    table.setStyle(tstyle)
    return table


# Retorna tabla de Muestra con su estilo
def style_punto(rawpunto, styles):
    tstyle = TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                         ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.lightgrey),
                         ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
    s = styles['BodyText']
    s.wordWrap = 'CJK'
    data = [[Paragraph(cell, s) for cell in row] for row in rawpunto]
    table = Table(data)
    table.setStyle(tstyle)
    return table
