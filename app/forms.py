# -*- coding: utf-8 -*-

__author__ = 'Juanjo'

from flask_wtf import Form
from flask_wtf.file import FileRequired
from wtforms import StringField, BooleanField, TextAreaField, FileField, DateField, DateTimeField, SelectField, SelectMultipleField, \
    DecimalField
from wtforms.validators import DataRequired, Length, regexp, Email
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
    nfecha = DateField(u'fecha', validators=[DataRequired(message=u'Ingrese una fecha de la campaña en formato YYYY-MM-DD')],
                      format='%Y-%m-%d')
    nresponsable = StringField('responsable', validators=[DataRequired(message=u'Responsable requerido')])
    nobjetivo = TextAreaField('objetivo')#, validators=[DataRequired(message=u'Ingrese un objetivo')])
    teledeteccion = TextAreaField('teledeteccion')
    especialidad = TextAreaField('especialidad')
    nfecha_pub = DateField(u'fecha', validators=[DataRequired(message=u'Ingrese una fecha de publicación del dato en formato YYYY-MM-DD')],
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
    id = StringField('id', validators=[DataRequired(message=u'Falta id')])
    nombre = StringField('nombre')
    fecha_hora = DateTimeField(u'fecha', validators=[DataRequired(message=u'Ingrese fecha y hora de la toma en formato YYYY-MM-DD HH:mm:ss')],
                      format='%Y-%m-%d %H:%M:%S')
    altura = StringField('altura')
    presion = StringField('presion')
    temp = StringField('temp')
    nubosidad = StringField('nubosidad')
    dir_viento = StringField('dir_viento')
    vel_viento = StringField('vel_viento')
    estado = StringField('estado')
    cant_tomas = StringField('cant_tomas')
    obs = TextAreaField('obs')
    oleaje = StringField('oleaje')
    foto = StringField('foto')
    muestra = StringField('muestra')
    lat_long = StringField('LatLong', validators=[DataRequired(message=u'Ingrese las coordenadas del Punto')])


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
    archivos = FileField('archivos', validators=[FileRequired(), regexp(r'^[^/\\]\.txt$')])

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
        elif self.validate_fottxt(filename):
            return 'fot'
        else:
            return False

    def validate_img(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def validate_radtxt(self, filename):
        return '.' in filename and \
               (filename.rsplit('.', 2)[1].lower() == 'rad' or filename.rsplit('.', 2)[1].lower() == 'asd') and \
               filename.rsplit('.', 1)[1].lower() == 'txt'

    def validate_radavgtxt(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 3)[1].lower() != 'rts' and \
               filename.rsplit('.', 2)[1].lower() == 'md' and \
               filename.rsplit('.', 1)[1].lower() == 'txt'

    def validate_radstdtxt(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 3)[1].lower() != 'rts' and \
               filename.rsplit('.', 2)[1].lower() == 'st' and \
               filename.rsplit('.', 1)[1].lower() == 'txt'

    def validate_reftxt(self, filename):
        return '.' in filename and \
               (filename.rsplit('.', 3)[1].lower() != 'sd' and filename.rsplit('.', 3)[1].lower() != 'md') and \
               filename.rsplit('.', 2)[1].lower() == 'rts' and \
               filename.rsplit('.', 1)[1].lower() == 'txt'

    def validate_refavgtxt(self, filename):
        return '.' in filename and \
               (filename.rsplit('.', 3)[1].lower() == 'rts' and filename.rsplit('.', 2)[1].lower() == 'md') or \
               (filename.rsplit('.', 3)[1].lower() == 'md' and filename.rsplit('.', 2)[1].lower() == 'rts') and \
               filename.rsplit('.', 1)[1].lower() == 'txt'

    def validate_refstdtxt(self, filename):
        return '.' in filename and \
               (filename.rsplit('.', 3)[1].lower() == 'rts' and filename.rsplit('.', 2)[1].lower() == 'st') or \
               (filename.rsplit('.', 3)[1].lower() == 'st' and filename.rsplit('.', 2)[1].lower() == 'rts') and \
               filename.rsplit('.', 1)[1].lower() == 'txt'

    def validate_fottxt(self, filename):
        return '.' in filename and \
               (filename.rsplit('-', 1)[1].lower() == 'fot.txt' or len(filename.rsplit('FOT')) > 1)

# Formulario de consulta
class ConsultarForm(Form):
    filtro = SelectMultipleField('filtro', choices=['Proyecto', 'Localidad', 'Fecha', 'Tipo Cobertura',
                                                    'Cobertura'])
    fuente = SelectField('fuente', coerce=int)
    tipo_cobertura = SelectField('tipo_cobertura', coerce=int)
    cobertura = SelectField('cobertura', coerce=int)
    localidad = SelectField('localidad', coerce=int)
    fecha_inicio = DateField(u'fecha_inicio', format='%d-%m-%Y')
    fecha_fin = DateField(u'fecha_fin',  format='%d-%m-%Y')


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
    id_fuente = SelectField('fuente', coerce=int, validators=[DataRequired(message=u'Seleccione una Fuente de Datos')])

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

# Formulario de Contacto
class ContactoForm(Form):
    nombre = StringField('nombre', validators=[DataRequired(message=u'Falta el nombre')])
    email = StringField('email', validators=[DataRequired(message=u'Falta el email'), Email(message=u'Ingrese un email con formato: ejemplo@dominio.com')])
    asunto = StringField('asunto', validators=[DataRequired(message=u'Falta el asunto')])
    mensaje = TextAreaField('mensaje', validators=[DataRequired(message=u'Falta el mensaje')])
