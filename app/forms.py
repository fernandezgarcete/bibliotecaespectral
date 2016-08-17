# -*- coding: utf-8 -*-
import datetime

__author__ = 'Juanjo'

from flask_wtf import Form
from flask_babel import gettext
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, BooleanField, TextAreaField, FileField, DateField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange
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
    userId = StringField('token')


# Formulario de edición de perfil de usuario
class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired(message=u'Este dato es requerido')])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

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
    nproyecto = SelectField('proyecto', coerce=int, validators=[DataRequired(message=u'Proyecto requerido')])
    nlocalidad = SelectField('localidad', coerce=int, validators=[DataRequired(message=u'Localidad requerida')])
    ncampania = StringField('campania', validators=[DataRequired(message=u'Campaña requerida')])
    nfecha = DateField(u'fecha', validators=[DataRequired(message=u'Ingrese una fecha')],
                      format='%d-%m-%Y')
    #ninstitucion = StringField('intitucion', validators=[DataRequired(message=u'Institución requerida')])
    nresponsable = StringField('responsable', validators=[DataRequired(message=u'Responsable requerido')])
    nobjetivo = TextAreaField('objetivo', validators=[DataRequired(message=u'Ingrese un objetivo')])
    # ntipo_cobertura = SelectField('tipo_cobertura', coerce=int)
    # ncobertura = SelectField('cobertura', coerce=int)
    ninstrumento = SelectField('instrumento', coerce=int)
    nespectralon = SelectField('espectralon', coerce=int)
    ngps = SelectField('gps', coerce=int, validators=[DataRequired(message=u'Describa GPS')])
    ncamara = SelectField('camara', coerce=int, validators=[DataRequired(message=u'Cámara utilizada')])

# Formulario Editar Campaña
class EditarCampForm(Form):
    eproyecto = SelectField('proyecto', coerce=int, validators=[DataRequired(message=u'Proyecto requerido')])
    elocalidad = SelectField('localidad', coerce=int, validators=[DataRequired(message=u'Localidad requerida')])
    ecampania = StringField('campania', validators=[DataRequired(message=u'Campaña requerida')])
    efecha = DateField(u'fecha', validators=[DataRequired(message=u'Ingrese una fecha')],
                      format='%d-%m-%Y')
    einstitucion = StringField('intitucion', validators=[DataRequired(message=u'Institución requerida')])
    eresponsable = StringField('responsable', validators=[DataRequired(message=u'Responsable requerido')])
    eobjetivo = TextAreaField('objetivo', validators=[DataRequired(message=u'Ingrese un objetivo')])
    etipo_cobertura = SelectField('tipo_cobertura', coerce=int)
    ecobertura = SelectField('cobertura', coerce=int)
    ecobertura_nueva = SelectField('cobertura', coerce=int)
    einstrumento = SelectField('instrumento', coerce=int)
    eespectralon = SelectField('espectralon', coerce=int)
    egps = SelectField('gps', coerce=int, validators=[DataRequired(message=u'Describa GPS')])
    ecamara = SelectField('camara', coerce=int, validators=[DataRequired(message=u'Cámara utilizada')])

# Formulario Consulta de Campaña
class ConsultaCampForm(Form):
    ccampania = SelectField('campania', coerce=int, validators=[DataRequired(message=u'Campaña requerida')])

# Formulario Nueva Cobertura
class NuevaCoberturaForm(Form):
    ncnombre = StringField('nombre', validators=[DataRequired(message=u'Ingrese un nombre')])
    ncid_tipocobertura = StringField('id_tipocobertura', validators=[DataRequired])
    ncaltura = StringField('altura')
    ncfenologia = StringField('fenologia')
    ncobservaciones = TextAreaField('observaciones')

# Formulario de archivo
class ArchivoForm(Form):
    archivo = FileField('archivo', validators=[FileRequired()])

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
