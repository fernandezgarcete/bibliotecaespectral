# -*- coding: utf-8 -*-
import datetime

__author__ = 'Juanjo'

from flask_wtf import Form
from flask_babel import gettext
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, BooleanField, TextAreaField, FileField, DateField, SelectField, SelectMultipleField, \
    RadioField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, regexp
from app.models import User
from config import ALLOWED_EXTENSIONS


# Formulario de inicio de sesión
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired(message=u'Este dato es requerido')])
    remember_me = BooleanField('remember_me', default=False)

# Formulario de inicio de sesión CONAE
class LoginConaeForm(Form):
    username = StringField('User', validators=[DataRequired(message=u'Este dato es requerido')])
    password = StringField('Password', validators=[DataRequired(message=u'Este dato es requerido')])


# Formulario de edición de perfil de usuario
class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired(message=u'Este dato es requerido')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Este dato es requerido')])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, orig_nombre, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
        self.orig_nombre = orig_nombre

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(
                'Este nickname tiene caracteres inválidos. Por favor use solo letras, números, puntos y guión bajo.')
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('Este nombre ya existe. Por favor ingrese otro.')
            return False
        return True


# Formulario de Posteos
class PostForm(Form):
    post = StringField('post', validators=[DataRequired(message=u'Este dato es requerido')])


# Formulario de busqueda
class SearchForm(Form):
    search = StringField('search', validators=[DataRequired(message=u'Este dato es requerido')])


# Formulario carga de Campaña
class NuevaCampForm(Form):
    id = StringField('id')
    nproyecto = SelectField('proyecto', coerce=int, validators=[DataRequired(message=u'Seleccione un Proyecto')])
    nlocalidad = SelectField('localidad', coerce=int, validators=[DataRequired(message=u'Seleccione una Localidad')])
    ncampania = StringField('campania', validators=[DataRequired(message=u'Campaña requerida')])
    nfecha = DateField(u'fecha', validators=[DataRequired(message=u'Ingrese una fecha de la campaña')],
                      format='%Y-%m-%d')
    nresponsable = StringField('responsable', validators=[DataRequired(message=u'Responsable requerido')])
    nobjetivo = TextAreaField('objetivo')#, validators=[DataRequired(message=u'Ingrese un objetivo')])
    nfecha_pub = DateField(u'fecha', validators=[DataRequired(message=u'Ingrese una fecha de publicación del dato')],
                      format='%Y-%m-%d')


# Formulario de Muestra
class MuestraForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    operador = StringField('operador')
    nombre = StringField('nombre')
    campania = StringField('campania')
    metodologia = SelectField('metodologia', coerce=int, validators=[DataRequired(message=u'Ingrese una Metodología')])
    fotometro = SelectField('fotometro', coerce=int, validators=[DataRequired(message=u'Ingrese un Fotómetro')])
    radiometro = SelectField('instrumento', coerce=int, validators=[DataRequired(message=u'Ingrese un Espectro-radiómetro')])
    espectralon = SelectField('espectralon', coerce=int, validators=[DataRequired(message=u'Ingrese un Patrón')])
    gps = SelectField('gps', coerce=int, validators=[DataRequired(message=u'Ingrese un GPS')])
    camara = SelectField('camara', coerce=int, validators=[DataRequired(message=u'Ingrese una Cámara')])
    tipo_cobertura = SelectField('tipo_cobertura', coerce=int, validators=[DataRequired(message=u'Ingrese un Tipo de Cobertura')])
    cobertura = SelectField('cobertura', coerce=int, validators=[DataRequired(message=u'Ingrese una Cobertura')])


# Formulario de Punto
class PuntoForm(Form):
    StringField('id', validators=[DataRequired(message=u'Falta id')])


# Formulario Auxiliar de cobertura
class CoberturaForm(Form):
    ecobertura = SelectMultipleField('cobertura', coerce=int, validators=[DataRequired(message=u'Ingrese una Cobertura')])
    ecobertura_nueva = SelectField('cobertura', coerce=int)

# Formulario Consulta de Campaña
class ConsultaCampForm(Form):
    campania = SelectField('campania', coerce=int, validators=[DataRequired(message=u'Campaña requerida')])


# Formulario Nueva Cobertura
class NuevaCoberturaForm(Form):
    ncnombre = StringField('nombre', validators=[DataRequired(message=u'Ingrese un nombre')])
    ncid_tipocobertura = StringField('id_tipocobertura', validators=[DataRequired])
    ncaltura = StringField('altura')
    ncfenologia = StringField('fenologia')
    ncobservaciones = TextAreaField('observaciones')


# Formulario de archivo
class ArchivoForm(Form):
    radiancias = FileField('radiancias', validators=[FileRequired(), regexp(r'^[^/\\]\.rad.txt$')])
    rads_avg = FileField('rads_avg', validators=[FileRequired(), regexp(r'^[^/\\]\.md.txt$')])
    rads_st = FileField('rads_st', validators=[FileRequired(), regexp(r'^[^/\\]\.st.txt$')])
    reflectancias = FileField('reflectancias', validators=[FileRequired(), regexp(r'^[^/\\]\.rts.txt$')])
    refs_avg = FileField('refs_avg', validators=[FileRequired(), regexp(r'^[^/\\]\.md.rts.txt$')])
    refs_st = FileField('refs_st', validators=[FileRequired(), regexp(r'^[^/\\]\.st.rts.txt$')])
    fotos = FileField('fotos', validators=[FileRequired()])
    fotometrias = FileField('fotometrias', validators=[FileRequired(), regexp(r'^[^/\\]\-FOT.txt$')])

    def validate_archivo(self, filename):
        if self.validate_img(filename):
            return 'img'
        elif self.validate_radtxt(filename):
            return 'rad'
        elif self.validate_radavgtxt(filename):
            return 'radavg'
        elif self.validate_radstdtxt(filename):
            return 'radstd'
        elif self.validate_reftxt(filename):
            return 'ref1'
        elif self.validate_refavgtxt(filename):
            return 'refavg'
        elif self.validate_refstdtxt(filename):
            return 'refstd'
        else:
            return False

    def validate_img(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def validate_radtxt(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 2)[1] == 'rad' and \
           filename.rsplit('.', 1)[1] == 'txt'

    def validate_radavgtxt(self, filename):
        return '.' in filename and \
           filename.rsplit('-', 1)[1] != 'refl.md.txt' and \
           filename.rsplit('.', 2)[1] == 'md' and \
           filename.rsplit('.', 1)[1] == 'txt'

    def validate_radstdtxt(self, filename):
        return '.' in filename and \
           filename.rsplit('-', 1)[1] != 'refl.st.txt' and \
           filename.rsplit('.', 2)[1] == 'st' and \
           filename.rsplit('.', 1)[1] == 'txt'

    def validate_reftxt(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 2)[1] == 'rts' and \
           filename.rsplit('.', 1)[1] == 'txt'

    def validate_refavgtxt(self, filename):
        return '.' in filename and \
           filename.rsplit('-', 1)[1] == 'refl.md.txt' and \
           filename.rsplit('.', 2)[1] == 'md' and \
           filename.rsplit('.', 1)[1] == 'txt'

    def validate_refstdtxt(self, filename):
        return '.' in filename and \
           filename.rsplit('-', 1)[1] == 'refl.st.txt' and \
           filename.rsplit('.', 2)[1] == 'st' and \
           filename.rsplit('.', 1)[1] == 'txt'

# Formulario de consulta
class ConsultarForm(Form):
    filtro = SelectMultipleField('filtro', choices=['Proyecto', 'Localidad', 'Fecha', 'Tipo Cobertura',
                                                    'Cobertura'])
    proyecto = SelectField('proyecto', coerce=int)#, validators=[DataRequired(message=u'Proyecto requerido')])
    localidad = SelectField('localidad', coerce=int)#, validators=[DataRequired(message=u'Localidad requerida')])
    # campania = SelectField('campania', coerce=int)#, validators=[DataRequired(message=u'Campaña requerida')])
    fecha_inicio = DateField(u'fecha_inicio', format='%d-%m-%Y')
    fecha_fin = DateField(u'fecha_fin',  format='%d-%m-%Y')
    tipo_cobertura = SelectField('tipo_cobertura', coerce=int)
    cobertura = SelectField('cobertura', coerce=int)
    # radiancia = BooleanField('radiancia', default=True)
    # radiancia_avg = BooleanField('radiancia_avg', default=False)
    # radiancia_std = BooleanField('radiancia_std', default=False)
    # reflectancia = BooleanField('reflectancia', default=False)
    # reflectancia_avg = BooleanField('reflectancia_avg', default=False)
    # reflectancia_std = BooleanField('reflectancia_std', default=False)

# Formulario de Metodologias
class MetodologiaForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Ingrese un nombre de metodología')])
    descripcion = TextAreaField('descripcion', validators=[DataRequired(message=u'Describa la descripción')])
    medicion = TextAreaField('medicion')
    cenit = DecimalField('angulo cenital', places=2)
    azimut = DecimalField('angulo azimutal', places=2)

# Formulario de Metodologias
class ProyectoForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Ingrese un nombre al proyecto')])
    descripcion = TextAreaField('descripcion')
    responsables = StringField('responsables')
    status = BooleanField('status', default=False)

# Formulario de Consulta de Descargas
class DescargaForm(Form):
    fecha_inicio = DateField(u'fecha_inicio', format='%d-%m-%Y')
    fecha_fin = DateField(u'fecha_fin',  format='%d-%m-%Y')

# Formulario de Tipo Cobertura
class TPForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Ingrese un nombre al tipo de cobertura')])

# Formulario de Tipo Cobertura
class CobForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Ingrese un nombre a la cobertura')])
    tipo_cobertura = SelectField('cobertura', coerce=int, validators=[DataRequired(message=u'Seleccione un tipo de cobertura')])
    altura = StringField('altura')
    fenologia = StringField('fenologia')
    observaciones = TextAreaField('observaciones')

# Formualario de Radiometro
class RadiometroForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    codigo = StringField('codigo', validators=[DataRequired(message=u'Falta código')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Falta nombre')])
    marca = StringField('marca', validators=[DataRequired(message=u'Falta marca')])
    modelo = StringField('modelo', validators=[DataRequired(message=u'Falta modelo')])
    nro_serie = StringField('nro_serie', validators=[DataRequired(message=u'Falta el número de serie')])
    rango_espectral = StringField('rango_espectral', validators=[DataRequired(message=u'Falta el rango espectral')])
    resolucion_espectral = StringField('resolucion_espectral', validators=[DataRequired(message=u'Falta la resolucion espectral')])
    ancho_banda = StringField('ancho_banda', validators=[DataRequired(message=u'Falta el ancho de banda')])
    tiempo_escaneo = StringField('tiempo_escaneo', validators=[DataRequired(message=u'Falta tiempo de escaneo')])
    reproducibilidad = StringField('reproducibilidad', validators=[DataRequired(message=u'Falta reproducibilidad de ancho de banda')])
    exactitud = StringField('exactitud', validators=[DataRequired(message=u'Falta exactitud de ancho de banda')])
    detector_vnir = StringField('detector_vnir', validators=[DataRequired(message=u'Falta detector VNIR')])
    detector_swir1 = StringField('detector_swir1')
    detector_swir2 = StringField('detector_swir2')
    noise_vnir = StringField('noise_vnir', validators=[DataRequired(message=u'Falta el noise equivalence radiance en VNIR')])
    noise_swir1 = StringField('noise_swir1')
    noise_swir2 = StringField('noise_swir2')
    largo_fibra = StringField('largo_fibra', validators=[DataRequired(message=u'Falta el largo de fibra optica')])
    fov = StringField('fov', validators=[DataRequired(message=u'Falta el FOV')])
    fov_cosenoidal = StringField('fov_cosenoidal')
    accesorio = TextAreaField('accesorio')

# Formulario de Espectralon
class PatronForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    codigo = StringField('codigo', validators=[DataRequired(message=u'Falta código')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Falta nombre')])
    marca = StringField('marca', validators=[DataRequired(message=u'Falta marca')])
    modelo = StringField('modelo', validators=[DataRequired(message=u'Falta modelo')])
    nro_serie = StringField('nro_serie', validators=[DataRequired(message=u'Falta el número de serie')])
    accesorio = TextAreaField('accesorio')

# Formulario de Fotometro
class FotometroForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    codigo = StringField('codigo', validators=[DataRequired(message=u'Falta código')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Falta nombre')])
    marca = StringField('marca', validators=[DataRequired(message=u'Falta marca')])
    modelo = StringField('modelo', validators=[DataRequired(message=u'Falta modelo')])
    nro_serie = StringField('nro_serie', validators=[DataRequired(message=u'Falta el número de serie')])
    accesorio = TextAreaField('accesorio')

# Formulario de Fotometro
class CamaraForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    codigo = StringField('codigo', validators=[DataRequired(message=u'Falta código')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Falta nombre')])
    marca = StringField('marca', validators=[DataRequired(message=u'Falta marca')])
    modelo = StringField('modelo', validators=[DataRequired(message=u'Falta modelo')])
    nro_serie = StringField('nro_serie', validators=[DataRequired(message=u'Falta el número de serie')])
    accesorio = TextAreaField('accesorio')

# Formulario de GPS
class GPSForm(Form):
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    codigo = StringField('codigo', validators=[DataRequired(message=u'Falta código')])
    nombre = StringField('nombre', validators=[DataRequired(message=u'Falta nombre')])
    marca = StringField('marca', validators=[DataRequired(message=u'Falta marca')])
    modelo = StringField('modelo', validators=[DataRequired(message=u'Falta modelo')])
    nro_serie = StringField('nro_serie', validators=[DataRequired(message=u'Falta el número de serie')])
    accesorio = TextAreaField('accesorio')