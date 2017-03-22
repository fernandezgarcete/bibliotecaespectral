# -*- coding: utf-8 -*-
import json
import os
import glob
from app.utils import geom2latlng
from reportlab.pdfgen import canvas
from reportlab.platypus.tableofcontents import TableOfContents

__author__ = 'Juanjo'

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, BaseDocTemplate, \
    PageTemplate, Frame, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as Ps
from reportlab.lib.units import inch, cm, mm
from config import basedir, UPLOAD_FOLDER


class MiDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kwargs)
        template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1')])
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        """ Registra entradas al TOC. """
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                level = 0
            elif style == 'Heading2':
                level = 1
            elif style == 'Heading3':
                level = 2
            else:
                return
            E = [level, text, self.page]
            bn = getattr(flowable, '_bookmarkName', None)
            if bn is not None:
                E.append(bn)
            self.notify('TOCEntry', tuple(E))


centered = Ps(name='centered',
              fontSize=18,
              leading=16,
              aligment=TA_CENTER,
              spaceAfter=20)

h1 = Ps(name='Heading1',
        fontSize=16,
        leading=16)

h2 = Ps(name='Heading2',
        spaceBefore=20,
        fontSize=14,
        leading=16)

h3 = Ps(name='Heading3',
        spaceBefore=20,
        fontSize=14,
        leading=16)

# Instancia del TOC
toc = TableOfContents()
toc.levelStyles = [
    Ps(fontname='Times-Bold', fontSize=14, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=10, leading=16),
    Ps(fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=5, leading=12),
    Ps(fontSize=12, name='TOCHeading3', leftIndent=60, firstLineIndent=-20, spaceBefore=2.5, leading=8)
]

# Funcion que crea el Heading
def doHeading(text, sty, array):
    from hashlib import sha1
    # nombre del bookmark
    bn = sha1((text + sty.name).encode('utf-8')).hexdigest()
    # modificar el texto del mensj para incluir un link con el nombre del bn
    h = Paragraph(text + '<a name="%s"/>' % bn, sty)
    # guardar el bn sobre el flowable para que lo pueda visualizar
    h._bookmarkName = bn
    array.append(h)


# Genera un resumen de la Campaña con sus Datos
def reporte_campania(camp):
    pdfdir = os.path.join(UPLOAD_FOLDER, 'C' + str(camp.id))
    doc = MiDocTemplate(os.path.join(pdfdir, camp.nombre+'.pdf'), rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    elements = []       # Lista que aloja todos los elementos del documento que se genera

    # Imagen del Logo
    dir = os.path.join(basedir, 'app')
    dir = os.path.join(dir, 'static')
    dir = os.path.join(dir, 'img')
    logo = os.path.join(dir, 'CONAE_chico_transp.png')
    img = Image(logo, 2*inch, 1.5*inch)

    elements.append(img)
    elements.append(Spacer(1, 12))

    # Estilos de alinamiento de parrafos
    styles = getSampleStyleSheet()
    styles.add(Ps(name='Justify', alignment=TA_JUSTIFY))
    styles.add(Ps(name='Center', alignment=TA_CENTER))

    # Titulo del documento
    ptxt = '<font size=18><b>Biblioteca Nacional de Firmas Espectrales</b></font>'
    elements.append(Paragraph(ptxt, styles['Center']))
    elements.append(Spacer(1, 24))
    elements.append(Spacer(1, 24))

    # Titulo del documento
    ptxt = '<b>Contenido</b>'
    elements.append(Paragraph(ptxt, centered))
    elements.append(toc)
    elements.append(PageBreak())

    # Seccion de datos de Campaña
    doHeading('Campaña', h1, elements)
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
        if len(cobs.split(',')) > 1:
            split = cobs.split(',')
            cobs = split[0] if split[1].replace(' ', '') == split[0] else cobs

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

    # Seccion de datos de Muestras
    if muestras:
        for i, m in enumerate(muestras):
            elements.append(Spacer(1, 12))
            doHeading(str(i+1)+'. Muestra', h2, elements)
            elements.append(Spacer(1, 12))
            data_muestra = raw_muestra(m)
            tabla_muestra = style_muestra(data_muestra, styles)
            elements.append(tabla_muestra)
            elements.append(Spacer(1, 12))

            # Sección de datos de cada punto si tiene
            if puntos[m.id]:
                latlngs = geom2latlng(puntos[m.id])
                for j, p in enumerate(puntos[m.id]):
                    doHeading(str(i+1)+'.'+str(j+1)+'.  Punto', h3, elements)
                    elements.append(Spacer(1, 12))
                    data_punto = raw_punto(p, latlngs)
                    tabla_punto = style_punto(data_punto, styles)
                    elements.append(tabla_punto)
                    elements.append(Spacer(1, 12))
                    tabla_fotos = [incluir_fotos(p)]
                    elements.append(Table(tabla_fotos)) if tabla_fotos[0] else ''
                    elements.append(Spacer(1, 12))

    # Al terminar de agregar los elementos se crea el documento
    doc.multiBuild(elements, canvasmaker=NumberedCanvas)
    return True


# Retorna la lista para la tabla de muestra
def raw_muestra(muestra):
    rawmuestra = [['<b>Muestra</b>', muestra.cobertura_muestra.nombre],
                  ['<b>Carpeta</b>', 'M'+str(muestra.id)],
                  ['<b>Proyecto</b>', muestra.campania_muestra.proyecto_campania.nombre],
                  ['<b>Pregunta de Teledectección</b>', muestra.campania_muestra.teledeteccion if muestra.campania_muestra.teledeteccion else '-'],
                  ['<b>Pregunta de Especialidad</b>', muestra.campania_muestra.especialidad if muestra.campania_muestra.especialidad else '-'],
                  ['<b>Espectro-radiómetro</b>', muestra.radiometro_muestra.nombre],
                  ['<b>Otros Instrumentos</b>', '<b>FOTOMETRO:</b> '+muestra.fotometro_muestra.nombre +
                   ', <br/><b>CAMARA:</b> '+muestra.camara_muestra.nombre+', <br/><b>GPS:</b> '+muestra.gps_muestra.nombre +
                   ', <br/><b>PATRON:</b> '+muestra.patron_muestra.nombre],
                  ['<b>Metodología</b>', muestra.metodo_muestra.nombre + '<br/>' + muestra.metodo_muestra.descripcion],
                  ['<b>Punto/s</b>', str(len(muestra.get_puntos()))]]
    return rawmuestra


# Retorna la lista para la tabla de punto
def raw_punto(punto, latlngs):
    latlng = json.loads(latlngs[punto.id])
    e = {'M': 'Malo', 'A': 'Aceptable', 'B': 'Bueno', 'MB': 'Muy Bueno', 'E': 'Excelente'}
    rawpunto = [['<b>Punto</b>', 'P'+str(punto.id)],
                ['<b>Fecha y Hora</b>', punto.fecha_hora.strftime('%Y-%m-%d %H:%S ART')],
                ['<b>Ubicación</b>', 'Latitud: '+str(latlng['lat']) + ' <br/>Longitud: '+str(latlng['lng'])],
                ['<b>Nubosidad</b>', str(punto.nubosidad) + ' %' if punto.nubosidad else '-'],
                ['<b>Estado</b>', e[punto.estado] if punto.estado in e else '-'],
                ['<b>Observaciones</b>', punto.observaciones if punto.observaciones else '-']]
    return rawpunto


# Retorna las fotos del Punto como vista previa
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


# Crea las vistas previas de fotos
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


# Retorna tabla Muestra con su estilo
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


# Retorna tabla Punto con su estilo
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

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 10)
        self.drawRightString(200*mm, 20*mm, "%d" % self._pageNumber)
