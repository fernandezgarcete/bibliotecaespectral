# -*- coding: utf-8 -*-
import datetime

__author__ = 'Juanjo'

from flask_wtf import Form
from flask_babel import gettext
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, BooleanField, TextAreaField, FileField, DateField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models import User
from config import ALLOWED_EXTENSIONS


# Formulario de inicio de sesión
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired(message=u'Este dato es requerido')])
    remember_me = BooleanField('remember_me', default=False)

# Formulario de inicio de sesión CONAE
class LoginConaeForm(Form):
    username = StringField('Usuario email', validators=[DataRequired(message=u'Este dato es requerido')])
    password = StringField('Password', validators=[DataRequired(message=u'Este dato es requerido')])
    userid = StringField('tocken')


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
                gettext('Este nickname tiene caracteres inválidos. Por favor use solo letras, números, puntos y guión bajo.')
            )
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append(gettext('Este nombre ya existe. Por favor ingrese otro.'))
            return False
        return True


# Formulario de Posteos
class PostForm(Form):
    post = StringField('post', validators=[DataRequired(message=u'Este dato es requerido')])


# Formulario de busqueda
class SearchForm(Form):
    search = StringField('search', validators=[DataRequired(message=u'Este dato es requerido')])


# Formulario carga de archivos
class CargarForm(Form):
    proyecto = StringField('proyecto', validators=[DataRequired(message=u'Proyecto requerido')])
    localidad = SelectField('localidad', coerce=int, validators=[DataRequired(message=u'Localidad requerida')])
    campania = StringField('campania', validators=[DataRequired(message=u'Campaña requerida')])
    fecha = DateField(u'fecha', validators=[DataRequired(message=u'Ingrese una fecha')],
                      format='%d-%m-%Y')
    institucion = StringField('intitucion', validators=[DataRequired(message=u'Institución requerida')])
    responsable = StringField('responsable', validators=[DataRequired(message=u'Responsable requerido')])
    objetivo = TextAreaField('objetivo', validators=[DataRequired(message=u'Ingrese un objetivo')])
    tipo_cobertura = SelectField('tipo_cobertura', coerce=int,
                                 choices=[(0,''),(1, 'Agricultura'), (2, 'Hidrología'), (3, 'Calibración'), (4, 'Laboratorio')],
                                 validators=[NumberRange(min=1)])
    cobertura = SelectField('cobertura', coerce=int,
                            choices=[(0,''),(1, 'Alfalfa'), (2, 'Maíz'), (3, 'Soja'), (4, 'Sorgo'), (5, 'Trigo'), (6, 'Lago'), (7, 'Río'), (8, 'Mar'), (9, 'Calibracion'), (10, 'Laboratorio')],
                            validators=[NumberRange(min=1)])
    instrumento = SelectField('instrumento', choices=[(0,''),(1, 'ASD-PRO Nuevo'), (2, 'ASD Antiguo')], coerce=int,
                              validators=[NumberRange(min=1)])
    espectralon = SelectField('espectralon', choices=[(0,''),(1, 'Maestro'), (2, 'Grande'), (3, 'Chico')], coerce=int,
                              validators=[NumberRange(min=1)])
    gps = StringField('gps', validators=[DataRequired(message=u'Describa GPS')])
    camara = StringField('camara', validators=[DataRequired(message=u'Cámara utilizada')])


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
            return 'ref'
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
    proyecto = proyecto = StringField('proyecto', validators=[DataRequired(message=u'Proyecto requerido')])
    localidad = StringField('localidad', validators=[DataRequired(message=u'Localidad requerida')])
    campania = StringField('campania', validators=[DataRequired(message=u'Campaña requerida')])
    fecha_inicio = DateField(u'fecha_inicio', validators=[DataRequired(message=u'Ingrese una fecha')],
                      format='%d-%m-%Y')
    fecha_fin = DateField(u'fecha_fin', validators=[DataRequired(message=u'Ingrese una fecha')],
                      format='%d-%m-%Y')
    tipo_cobertura = SelectField('tipo_cobertura', coerce=int,
                                 choices=[(0,''), (1, 'Agricultura'), (2, 'Hidrología'), (3, 'Calibración'), (4, 'Laboratorio')],
                                 validators=[NumberRange(min=1)])
    cobertura = SelectField('cobertura', coerce=int,
                            choices=[(0,''), (1, 'Alfalfa'), (2, 'Maíz'), (3, 'Soja'), (4, 'Sorgo'), (5, 'Trigo'), (6, 'Lago'), (7, 'Río'), (8, 'Mar'), (9, 'Calibracion'), (10, 'Laboratorio')],
                            validators=[NumberRange(min=1)])
    radiancia = BooleanField('radiancia', default=True)
    radiancia_avg = BooleanField('radiancia_avg', default=False)
    radiancia_std = BooleanField('radiancia_std', default=False)
    reflectancia = BooleanField('reflectancia', default=False)
    reflectancia_avg = BooleanField('reflectancia_avg', default=False)
    reflectancia_std = BooleanField('reflectancia_std', default=False)
