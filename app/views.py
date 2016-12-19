# -*- coding: utf-8 -*-

from datetime import datetime
import json
import os
import re
import requests
import traceback
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import get_debug_queries
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import gettext
from app import app, db, lm, oid, babel
from .emails import follower_notification, error_notification, contact_notification
from .forms import LoginForm, EditForm, PostForm, SearchForm, ConsultarForm, ArchivoForm, LoginConaeForm, NuevaCoberturaForm, \
    MetodologiaForm, DescargaForm, ProyectoForm, TPForm, CobForm, RadiometroForm, PatronForm, FotometroForm, CamaraForm, \
    GPSForm, PuntoForm, ContactoForm
from .models import User, Post, Localidad, TipoCobertura, Cobertura, Campania, Proyecto, \
    Muestra, Metodologia, Descarga, Radiometro, Patron, Fotometro, Camara, Gps, Punto
from .translate import microsoft_translate
from .utils import cargar_archivo, ini_consulta_camp, ini_nuevo_form, ini_actualizar_form, \
    actualizar_tp, utf_to_ascii, tabular_descargas, ini_muestra_form, limpia_responsables, \
    get_page, default_punto, geom2latlng, detalle_archivos, checkRecaptcha
from config import POST_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, UPLOAD_FOLDER, DOCUMENTS_FOLDER, DEVLOGOUT, \
    CAMPAIGNS_FOLDER, DATABASE_QUERY_TIMEOUT, PROTOCOLOS_FOLDER, FICHAS_FOLDER, SECRET_KEY_CAPTCHA, SITE_KEY_CAPTCHA
from guess_language import guessLanguage
from .oauth import OAuthSignIn, ConaeSignIn
import geoalchemy2.functions as geofunc



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    user = g.user   # Se asigna el usuario de sesión actual
    form = PostForm()
    if form.validate_on_submit():
        language = guessLanguage(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data,
                    timestamp=datetime.utcnow(),
                    author=g.user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(gettext('Su comentario ha sido posteado!'), 'success')
        return redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, POST_PER_PAGE, False)
    return render_template('index.html',
                           title='Biblioteca Espectral CONAE',
                           user=user,
                           form=form,
                           posts=posts)


# Verificaciones antes del inicio de sesión
@app.before_request
def before_request():
    g.user = current_user
    #if g.user.is_anonymous:
    #    g.user = User.query.filter_by(email='anonymous@example.com').first()
    #else:
    #    g.user = current_user   # agregamos a g.user al usuario de la sesión actual antes de cada request.
    if g.user.is_authenticated:                 # Si el usuario está autenticado,
        g.user.last_seen = datetime.utcnow()    # registramos su última visita
        db.session.add(g.user)                  # cargamos a la BD toda la información del usuario
        db.session.commit()                     # y confirmamos la persistencia en la BD.
        g.search_form = SearchForm()
    g.locale = get_locale()


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning(
                "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                (query.statement, query.parameters, query.duration,
                 query.context))
    return response


# Inicio de sesión API Conae
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    conae_sign = ConaeSignIn()
    if request.method == 'POST':
        form = LoginConaeForm()
        try:
            form.username.data = request.form['username']
            form.password.data = request.form['password']
            form.csrf_token.data = request.form['csrf_token']
        except:
            pass
        if form.validate_on_submit():
            datos = conae_sign.login(form)
            if datos:
                conae_after_login(datos)
            else:
                return redirect(url_for('login'))
        else:
            flash('Falta Completar:', 'error')
    return render_template('login.html')


# Renderizar Formulario Login
@app.route('/loginform')
def loginform():
    form = LoginConaeForm()
    return render_template('login_form.html', form=form)


# Inicio de sesión del usuario
@app.route('/loginoid', methods=['GET', 'POST'])
@oid.loginhandler       # Comunica a Flask-OpenID que es la función de Inicio de Sesión
def loginoid():
    # Se utiliza la variable "g" de Flask para guardar valores globales. En este caso la sesión del usuario se guarda
    # en la variable g.user
    #if g.user is not None and g.user.is_authenticated:  # Verifica si el usuario ya inició sesión previamente
        #return redirect(url_for('index'))               # Si se cumple envia al inicio
    # Caso contrario se prepara el formulario de sesión
    form = LoginForm()
    if form.validate_on_submit():                                               # Si el formulario es válido,
        session['remember_me'] = form.remember_me.data                          # se carga el valor de Recuerdame y
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])   # se intenta iniciar sesión con OID
    return render_template('login.html',
                           title='Ingresar',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def conae_after_login(datos):
    user = User.query.filter_by(email=datos['email']).first()
    if user is None:                                    # Si no existe, registraremos al nuevo usuario en la BD.
        print('Nombre')
        print(datos['nombre'])
        nickname = datos['nombre']+' '+datos['apellido']# Se intenta obtener el nickname de la respuesta.
        print(nickname)
        if nickname is None or nickname == "":          # Si no se obtiene de la respuesta "resp",
            nickname = datos['email'].split('@')[0]     # se entresaca el nickname desde el email hasta el '@'
        nickname = User.make_valid_nickname(nickname)   # Validaciones previas a la aceptacion del nickname.
        nickname = User.make_unique_nickname(nickname)  # No aceptar duplicados.
        uid = User.query.order_by(User.id.desc()).first().id + 1
        nombre = re.sub("([a-z])([A-Z])", "\g<1> \g<2>", nickname)  # Separar CamelCase con espacios
        user = User(social_id='sinredsocial'+str(uid), nickname=nickname, email=datos['email'], nombre=nombre)# Obtenidos los datos, creamos User con el nickname y email
        db.session.add(user)        # Agregamos a la sesión de la Base de Datos
        db.session.commit()         # Confirmamos la persistencia del nuevo Usuario en la BD.
        ### hagamos al usuario seguidor de si mismo para visualizar sus post ###
        db.session.add(user.follow(user))
        db.session.commit()
    # Se crea una variable para guardar el dato recuerdame
    remember_me = False
    if 'remember_me' in session:                # Si recuerdame está en la sesión,
        remember_me = session['remember_me']    # se guarda el valor de la variable
        session.pop('remember_me', None)        # y luego se saca del array de la sesión
    login_user(user, remember=remember_me)       # Iniciamos sesión con el Usuario y recordamos si se indica
    # Finalmente redigimos al inicio con sesión iniciada.
    return redirect(request.args.get('next') or url_for('index'))


# Recibiendo la respuesta del intento de inicio de sesión
def after_login(resp):
    if resp.email is None or resp.email == "":          # Si la respuesta "resp" devuelve vacío el campo email, no se
        flash('Inicio de sesión inválido. Por favor intente de nuevo.', 'error') # inició sesión y se pide de vuelta
        return redirect(url_for('login'))                               # otro intento
    # En caso exitoso se busca al usuario en la BD por email.
    user = User.query.filter_by(email=resp.email).first()
    if user is None:                                    # Si no existe, registraremos al nuevo usuario en la BD.
        nickname = resp.nickname                        # Se intenta obtener el nickname de la respuesta.
        if nickname is None or nickname == "":          # Si no se obtiene de la respuesta "resp",
            nickname = resp.email.split('@')[0]         # se entresaca el nickname desde el email hasta el '@'
        nickname = User.make_valid_nickname(nickname)   # Validaciones previas a la aceptacion del nickname.
        nickname = User.make_unique_nickname(nickname)  # No aceptar duplicados.
        user = User(social_id='sinredsocial',nickname=nickname, email=resp.email)# Obtenidos los datos, creamos User con el nickname y email
        db.session.add(user)        # Agregamos a la sesión de la Base de Datos
        db.session.commit()         # Confirmamos la persistencia del nuevo Usuario en la BD.
        ### hagamos al usuario seguidor de si mismo para visualizar sus post ###
        db.session.add(user.follow(user))
        db.session.commit()
    # Se crea una variable para guardar el dato recuerdame
    remember_me = False
    if 'remember_me' in session:                # Si recuerdame está en la sesión,
        remember_me = session['remember_me']    # se guarda el valor de la variable
        session.pop('remember_me', None)        # y luego se saca del array de la sesión
    login_user(user, remember=remember_me)       # Iniciamos sesión con el Usuario y recordamos si se indica
    # Finalmente redigimos a la siguient pag o al inicio con sesión iniciada.
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@oid.after_login
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


# Cerrando sesión del usuario
@app.route('/logout')
def logout():
    logout_user()                       # Usamos la función de cerrar sesión de Flask
    session.pop('id', None)
    try:
        requests.get(DEVLOGOUT + session['userid'])
    except:
        pass
    session.pop('userid', None)
    return redirect(url_for('index'))   # Redirigimos al inicio de sesión


# Vista del perfil de usuario
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()  # Carga datos del usuario desde la BD en "user".
    if user is None:                                    # Si no existe el usuario,
        flash(gettext('Usuario %s no encontrado.' % nickname), 'info')   # muestra un mensaje y
        return redirect(url_for('index'))               # envia de vuelta al inicio de sesión.
    posts = user.posts.paginate(page, POST_PER_PAGE, False)
    return render_template('user.html',     # Envía el template html del usuario con sus datos y posteos
                           user=user,
                           posts=posts)


# Vista de la edición de perfil
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname, g.user.nombre)   # Cargamos un formulario del tipo EditForm
    if form.validate_on_submit():               # Si el formulario es válido
        g.user.nickname = form.nickname.data    # cargamos el valor del nombre en nickname global
        g.user.about_me = form.about_me.data    # y la descripción personal correspondiente.
        db.session.add(g.user)          # Agregamos a la sesión de la BD para actualizarla
        db.session.commit()             # y confirmamos los cambios en la BD.
        flash('Sus cambios han sido guardados.', 'success')    # Se emite un mensaje de confirmación al usuario
        return redirect(url_for('edit'))     # y se redirige a la misma página
    else:   # caso contrario
        form.nickname.data = g.user.nickname    # se dejan los datos como están en la sesión actual
        form.about_me.data = g.user.about_me
        form.nombre.data = g.user.nombre
    return render_template('edit.html', form=form)  # Finalmente se redirige a la pag de edición con el formulario


# Contemplando error Page Not Found - 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# Contemplando error Internal Error - 500
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()       # Deshacer cambios en la BD
    error_notification(g.user)  # Enviar mail al admin
    return render_template('500.html'), 500


@app.route('/error')
def error_test():
    e = 1/0
    return render_template(url_for('index'))

# Vista de seguir a un usuario
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()  # Traemos el usuario requerido desde la BD
    if user is None:
        flash('Usuario %s no encontrado.' % nickname, 'info')       # Si no se encuentra, se muestra un mensaje y se reenvia
        return redirect(url_for('index'))                   # al inicio.
    if user == g.user:
        flash('No puede seguirse a si mismo!', 'error')              # Evitamos volver a seguirse ya que se encuentra seguido
        return redirect(url_for('user', nickname=nickname)) # por si mismo al crear al usuario.
    u = g.user.follow(user)
    if u is None:
        flash('No puede seguir a '+nickname+'.', 'error')            # Si se produce un error
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)                                       # en caso que esté correcto, agregamos a la BD,
    db.session.commit()                                     # confirmamos las modificaciones y
    flash('Ahora est&aacutes siguiendo a '+nickname+'.', 'success')    # mostramos un mensaje de seguimiento.
    follower_notification(url_for('user', nickname=nickname))# Enviamos una notificacion de mail.
    return redirect(url_for('user', nickname=nickname))


# Vista de dejar de seguir a un usuario
@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('Usuario %s no encontrado.' % nickname, 'info')
        return redirect(url_for('index'))
    if user == g.user:
        flash('No puedes dejar de seguirte a ti mismo.', 'error')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('No puedes dejar de seguir a '+nickname+'.', 'error')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('Has dejado de seguir a '+nickname+'.', 'success')
    return redirect(url_for('user', nickname=nickname))


# Vista de busqueda
@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


# Vista de resultados de busqueda
@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)

# Vista de idiomas
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


# Vista para la traduccion
@app.route('/translate', methods=['POST'])
@login_required
def translate():
    return jsonify({
        'text': microsoft_translate(
            request.form['text'],
            request.form['sourceLang'],
            request.form['destLang']
        )
    })


# Vista para borrar posteos
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash(gettext('Posteo no encontrado.'), 'info')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash(gettext('No puede borrar posteos de otros.'), 'error')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash(gettext('Su posteo ha sido borrado.'), 'success')
    return redirect(url_for('foro'))


# Vista para cargar archivo
@app.route('/resp', methods=['GET', 'POST'])
def resp():
    render_template('resultado.html')


# Carga de archivos paso 1
@app.route('/cargar', methods=['GET'])
@login_required
def cargar():
    return render_template('cargar.html')

# Gestiones Administrativas
@app.route('/administrativo', methods=['GET'])
@login_required
def administrativo():
    return render_template('administrativo.html')

# Carga de campaña paso 1
@app.route('/cargar/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    form_n = ini_nuevo_form()
    if request.method == 'POST':
        form_n.id.data = 0
        if form_n.nfecha.raw_data[0] != '':
            try:
                form_n.nfecha.data = datetime.strptime(form_n.nfecha.raw_data[0], '%Y-%m-%d').date()
            except:
                pass
        if form_n.nfecha_pub.raw_data[0] != '':
            try:
                form_n.nfecha_pub.data = datetime.strptime(form_n.nfecha_pub.raw_data[0], '%Y-%m-%d').date()
            except:
                pass
        if form_n.validate_on_submit():
            c = Campania()
            if c.agregar(form_n):
                flash('Campaña guardada.', 'success')
            else:
                print('Error')
    return render_template('cargar_n.html',
                           form_n=form_n)


# Carga de Muestras
@app.route('/cargar/campania/muestra', methods=['GET', 'POST'])
@app.route('/cargar/campania/muestra/<int:page>', methods=['GET', 'POST'])
@login_required
def muestra(page=1):
    id = int(request.args.get('id').split('-')[0])
    form = ini_muestra_form(id)
    muestras = Muestra.query.join(Cobertura, TipoCobertura).filter(Muestra.id_campania==id, Muestra.deleted==False).\
        order_by(Muestra.nombre).paginate(page, POST_PER_PAGE, False)
    camp = Campania.query.join(Proyecto, Localidad).filter(Campania.id==id).first()
    camp.responsables = limpia_responsables(camp.responsables)
    if request.method == 'POST':
        if form.validate_on_submit():
            m = Muestra()
            form.operador.data = camp.responsables
            if m.agregar(form):
                flash('Muestra guardada.', 'success')
            else:
                print('Error')
    return render_template('muestra.html', form=form, muestras=muestras, camp=camp)


# Borrar una muestra existente
@app.route('/cargar/campania/muestra/borrar/<int:id>')
@login_required
def borrar_muestra(id):
    muestra = Muestra.query.get(id)
    if muestra is None:
        flash('No se ha podido eliminar la muestra', 'error')
        return redirect(url_for('muestra', id=muestra.id_campania))
    muestra.deleted = True
    db.session.add(muestra)
    db.session.commit()
    flash(gettext('La muestra ha sido borrada.'), 'success')
    return redirect(url_for('muestra', id=muestra.id_campania))

# Actualizar la cobertura
@app.route('/cargar/actualizarcob')
def actualizarcob():
    arg = request.args.get('id')
    if 'idtp' in request.args:
        idtp = int(request.args.get('idtp'))
        if arg is None:
            form = actualizar_tp(idtp)
            return render_template('actualizarcob.html', form=form)
    return render_template('404.html'), 404


@app.route('/cargar/existente', methods=['GET', 'POST'])
@login_required
def consulta_existente():
    form_c = ini_consulta_camp()
    if request.method == 'POST':
        if form_c.validate_on_submit():
            id = form_c.campania.data
            return redirect(url_for('editar', id=id))
        else:
            flash('Falta Completar:', 'error')
            return render_template('cargar_c.html',
                                   form_c=form_c)
    return render_template('cargar_c.html',
                           form_c=form_c)


@app.route('/cargar/campania/muestra/punto', methods=['GET', 'POST'])
@app.route('/cargar/campania/muestra/punto/<int:page>', methods=['GET', 'POST'])
@login_required
def punto(page=1):
    idm = int(request.args.get('idm').split('-')[0])
    idc = int(request.args.get('idc').split('-')[0])
    form = PuntoForm()
    puntos = Punto.query.join(Muestra).filter(Punto.id_muestra==idm, Punto.deleted==False).order_by(Punto.id)\
        .paginate(page, POST_PER_PAGE, False)
    muestra = Muestra.query.join(Cobertura).filter(Muestra.id==idm).first()
    tp = TipoCobertura.query.filter_by(id=muestra.cobertura_muestra.id_tipocobertura).first()
    camp = Campania.query.join(Proyecto, Localidad).filter(Campania.id==idc).first()
    camp.responsables = limpia_responsables(camp.responsables)
    form.muestra.data = muestra.id
    latlngs = geom2latlng(puntos.items)
    if request.method == 'POST':
        if form.fecha_hora.data != '':
            try:
                if len(form.fecha_hora.raw_data[0].rsplit(':')) > 2:
                    try:
                        form.fecha_hora.data = datetime.strptime(form.fecha_hora.raw_data[0], '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
                else:
                    form.fecha_hora.raw_data[0] += ':00'
                    try:
                        form.fecha_hora.data = datetime.strptime(form.fecha_hora.raw_data[0], '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
            except:
                pass
        if form.validate_on_submit():
            form = default_punto(form)
            p = Punto()
            if p.agregar(form):
                flash('Punto guardado.', 'success')
            else:
                print('Error')
    return render_template('punto.html', form=form, puntos=puntos, muestra=muestra, camp=camp, tp=tp, latlngs=latlngs)


# carga archivos de radiancia
@app.route('/cargar/campania/muestra/punto/radiancia', methods=['GET','POST'])
@login_required
def radiancia():
    idm = int(request.args.get('idm').split('-')[0])
    idc = int(request.args.get('idc').split('-')[0])
    idp = int(request.args.get('idp').split('-')[0])
    archivoform = ArchivoForm()
    punto = Punto.query.join(Muestra).filter(Punto.id==idp, Punto.deleted==False).first()
    muestra = Muestra.query.join(Cobertura).filter(Muestra.id==idm).first()
    tp = TipoCobertura.query.filter_by(id=muestra.cobertura_muestra.id_tipocobertura).first()
    camp = Campania.query.join(Proyecto, Localidad).filter(Campania.id==idc).first()
    camp.responsables = limpia_responsables(camp.responsables)
    if request.method == 'POST':
        if archivoform.validate_on_submit():
            archivos = request.files.getlist('archivo')
            lugar = UPLOAD_FOLDER + re.findall("'([^']*)'", str(g.user))[0]
            count_rad=0
            count_radavg=0
            count_radstd=0
            count_ref=0
            count_refavg=0
            count_refstd=0
            count_img=0
            for a in archivos:
                file_name = secure_filename(a.filename)
                if len(file_name) > 0:
                    tipo = archivoform.validate_archivo(file_name)
                    if tipo:
                        verif = cargar_archivo(lugar, file_name, tipo, a)
                        if verif == 1:
                            flash('Archivo Radiancia cargado: '+file_name, 'success')
                            count_rad +=1
                        elif verif == 2:
                            flash('Archivo Radiancia Promedio cargado: '+file_name, 'success')
                            count_radavg +=1
                        elif verif == 3:
                            flash('Archivo Radiancia Desviación Estándar cargado: '+file_name, 'success')
                            count_radstd +=1
                        elif verif == 4:
                            flash('Archivo Reflectancia cargado: '+file_name, 'success')
                            count_ref +=1
                        elif verif == 5:
                            flash('Archivo Reflectancia Promerdio cargado: '+file_name, 'success')
                            count_refavg += 1
                        elif verif == 6:
                            flash('Archivo Reflectancia Desviación Estándar cargado: '+file_name, 'success')
                            count_refstd +=1
                        elif verif == 7:
                            flash('Archivo Imagen cargado: '+file_name, 'success')
                            count_img += 1
                    else:
                        flash('El archivo: '+file_name+' no es archivo de Radiancia, Reflectancia o Imagen válido.\n'+
                              'Radiancia: ".rad.txt", ".md.txt", ".st.txt"\n'+
                              'Reflectancia: ".rts.txt", "-refl.md.txt", "-refl.st.txt"\n'+
                              'Imagen: ".png", ".jpg", ".jpeg"', 'error')
            if count_rad == 0:
                flash('No ingresó ningún archivo de Radiancia', 'info')
            if count_radavg == 0:
                flash('No ingresó ningún archivo de Radiancia Promedio', 'info')
            if count_radstd == 0:
                flash('No ingresó ningún archivo de Radiancia Desviación Estándar', 'info')
            if count_ref == 0:
                flash('No ingresó ningún archivo de Reflectancia', 'info')
            if count_refavg == 0:
                flash('No ingresó ningún archivo de Reflectancia Promedio', 'info')
            if count_refstd == 0:
                flash('No ingresó ningún archivo de Reflectancia Desviación Estándar', 'info')
            if count_img == 0:
                flash('No ingresó ningún archivo de Imagen', 'info')
            # if count_rad>0 and count_radavg>0 and count_radstd>0 and count_ref>0 and count_refavg>0 and count_refstd>0 and form_e.validate_on_submit():
        if not archivoform.validate_on_submit():
            flash('Falta Completar:', 'error')
    return render_template('radiancia.html', camp=camp, muestra=muestra, tp=tp, archivoform=archivoform, punto=punto)

@app.route('/editar/nueva_cobertura', methods=['GET', 'POST'])
@login_required
def nueva_cobertura():
    form = NuevaCoberturaForm()
    if request.method == 'POST':
        nombre = form.ncnombre.data
        id_tipocobertura = int(form.ncid_tipocobertura.data)
        try:
            altura = float(form.ncaltura.data)
        except:
            altura = 0.0
        fenologia = form.ncfenologia.data
        observaciones = form.ncobservaciones.data
        if id_tipocobertura == 0:
            return jsonify({'cob': 'error', 'error': 'Antes de crear la Cobertura, cierre esta ventana \n '
                                                     'y elija un Tipo de Cobertura desde formulario anterior.'})
        if nombre is None or nombre == '':
            return jsonify({'cob': 'error', 'error': 'Ingrese un nombre para la Cobertura'})
        try:
            cob = Cobertura(nombre=nombre.upper(),
                            id_tipocobertura=id_tipocobertura,
                            altura=altura,
                            fenologia=fenologia,
                            observaciones=observaciones)

            db.session.add(cob)
            db.session.commit()
            return jsonify({'cob': cob.nombre})
        except:
            traceback.print_exc()
            db.session.rollback()
            return jsonify({'cob': 'error',
                            'error': 'Datos invalidos.'})

    return render_template('nc_form.html', form=form)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    form_e = ini_nuevo_form()
    camp = Campania.query.filter_by(id=id).first()
    camps = Campania.query.filter_by(deleted=False).order_by(Campania.nombre)
    camps = Campania.query.filter_by(deleted=False).order_by(Campania.nombre).paginate(get_page(camp, camps, POST_PER_PAGE),
                                                                                POST_PER_PAGE, False)
    if request.method == 'POST':
        form_e.id.data = id
        if form_e.ncampania.raw_data[0] != '':
            try:
                form_e.ncampania.data = form_e.ncampania.raw_data[0]
            except:
                pass
        if form_e.nfecha.raw_data[0] != '':
            try:
                form_e.nfecha.data = datetime.strptime(form_e.nfecha.raw_data[0], '%Y-%m-%d').date()
            except:
                pass
        if form_e.nfecha_pub.raw_data[0] != '':
            try:
                form_e.nfecha_pub.data = datetime.strptime(form_e.nfecha_pub.raw_data[0], '%Y-%m-%d').date()
            except:
                pass
        if form_e.validate_on_submit():
            c = Campania()
            if c.agregar(form_e):
                flash('Campaña guardada.', 'success')
            else:
                print('Error')
        return render_template('editar.html', form_e=form_e, camps=camps, camp=camp)
    return render_template('editar.html', form_e=form_e, camps=camps, camp=camp)

# mapa consulta
@app.route('/consultar/mapa', methods=['GET', 'POST'])
def mapa():
    if request.method == 'POST':
        nom = request.form.get('loc')
        loc = Localidad.query.filter_by(nombre=nom, deleted=False).first()
        camps = Campania.query.filter(Campania.id_localidad == loc.id, Campania.deleted == False).all()
        criterios = {'Localidad': loc.nombre}
        nombres = []
        for c in camps:
            nombres.append(c.nombre)
        return resultado(nombres, criterios)
    return redirect(url_for('consultar'))


@app.route('/punto/mapa', methods=['GET'])
@login_required
def punto_map():
    return render_template('punto_map.html')


# enviar localidades
@app.route('/consultar/mapa/loc', methods=['GET'])
def loc():
    jloc = dict(db.session.query(Localidad.nombre, geofunc.ST_AsGeoJSON(Localidad.geom)).filter_by(deleted=False).all())
    gloc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(value),
                "properties": {"name": key},
            } for key, value in jloc.items()
        ]
    }
    return jsonify(gloc)

# Consulta de datos
@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    form = ConsultarForm()
    form.cobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.filter_by(deleted=False).order_by('nombre')]
    form.cobertura.choices.insert(0, (0, ''))
    form.localidad.choices = [(l.id, l.nombre) for l in Localidad.query.filter_by(deleted=False).order_by('nombre')]
    form.localidad.choices.insert(0, (0, ''))
    form.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.filter_by(deleted=False).order_by('nombre')]
    form.tipo_cobertura.choices.insert(0, (0, ''))
    if request.method == 'POST':
        loc = form.localidad.data
        cob = form.cobertura.data
        tp = form.tipo_cobertura.data
        fi = form.fecha_inicio.data
        ff = form.fecha_fin.data
        camps = []
        criterios = {}
        if loc == 0 and cob == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.filter_by(deleted=False).order_by(Campania.nombre.desc()).all()
        if loc > 0 and cob == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.filter(Campania.id_localidad == loc, Campania.deleted == False).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
        if loc > 0 and fi is not None and ff is not None and cob == 0 and tp == 0:
            camps = Campania.query.filter(Campania.id_localidad == loc, Campania.fecha >= fi, Campania.fecha <= ff,
                                          Campania.deleted == False).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if loc > 0 and tp > 0 and cob == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   #Campania.deleted == False, Cobertura.deleted == False,
                                                                   Cobertura.id_tipocobertura == tp).all()
            print(camps)
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
        if loc > 0 and cob > 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra).filter(Campania.id_localidad == loc, Campania.deleted is False,
                                                        Muestra.id_cobertura == cob).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if fi is not None and loc == 0 and tp == 0 and cob == 0 and ff is None:
            camps = Campania.query.filter(Campania.fecha >= fi).all()
            criterios['Fecha Inicio'] = fi
        if ff is not None and loc == 0 and cob == 0 and tp == 0 and fi is None:
            camps = Campania.query.filter(Campania.fecha <= ff).all()
            criterios['Fecha Fin'] = ff
        if fi is not None and ff is not None and cob == 0 and tp == 0 and loc == 0:
            camps = Campania.query.filter(Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if cob > 0 and loc == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra).filter(Muestra.id_cobertura == cob).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if cob > 0 and fi is not None and ff is not None and loc == 0 and tp == 0:
            camps = Campania.query.join(Muestra).filter(Campania.fecha >= fi, Campania.fecha <= ff,
                                                        Muestra.id_cobertura == cob).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if tp > 0 and loc == 0 and cob == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Cobertura.id_tipocobertura == tp).all()
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
        if tp > 0 and fi is not None and ff is not None and loc == 0  and cob == 0:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.fecha >= fi, Campania.fecha <= ff,
                                                                   Cobertura.id_tipocobertura == tp).all()
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if tp > 0 and cob > 0 and loc == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if tp > 0 and cob > 0 and loc > 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if tp > 0 and loc > 0 and fi is not None and ff is not None and cob == 0:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if tp > 0 and cob > 0 and fi is not None and ff is not None and loc == 0:
            camps = Campania.query.join(Muestra, Cobertura).filter(Muestra.id_cobertura == cob,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if loc > 0 and cob > 0 and fi is not None and ff is not None and tp == 0:
            camps = Campania.query.join(Muestra).filter(Muestra.id_cobertura == cob, Campania.id_localidad == loc,
                                                        Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if tp > 0 and cob > 0 and loc > 0 and fi is not None and ff is not None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   Campania.fecha >= fi,
                                                                   Campania.fecha <= ff,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        nombres = []
        for c in camps:
            nombres.append(c.nombre)
        return resultado(nombres, criterios)
    return render_template('consultar.html', form=form)


# Consultar Descargas
@app.route('/consultar/descargas', methods=['GET', 'POST'])
@login_required
def descargas():
    form = DescargaForm()
    if request.method == 'POST':
        fi = form.fecha_inicio.data
        ff = form.fecha_fin.data
        descargas = []
        if fi is None and ff is None:
            descargas = Descarga.query.join(User).all()
        if fi is None and ff is not None:
            descargas = Descarga.query.join(User).filter(Descarga.fecha_descarga <= ff).all()
        if fi is not None and ff is None:
            descargas = Descarga.query.join(User).filter(Descarga.fecha_descarga >= fi).all()
        if fi is not None and ff is not None:
            descargas = Descarga.query.join(User).filter(Descarga.fecha_descarga >= fi, Descarga.fecha_descarga <= ff).all()
        tabla = tabular_descargas(descargas)
        return render_template('consultar_descargas.html', form=form, tabla=tabla)
    return render_template('consultar_descargas.html', form=form)

# Vista del Foro
@app.route('/', methods=['GET', 'POST'])
@app.route('/foro', methods=['GET', 'POST'])
@app.route('/foro/<int:page>', methods=['GET', 'POST'])
@login_required
def foro(page=1):
    user = g.user   # Se asigna el usuario de sesión actual
    form = PostForm()
    if form.validate_on_submit():
        language = guessLanguage(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data,
                    timestamp=datetime.utcnow(),
                    author=g.user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(gettext('Su comentario ha sido posteado!'), 'success')
        return redirect(url_for('foro'))
    posts = g.user.followed_posts().paginate(page, POST_PER_PAGE, False)
    return render_template('foro.html',
                           title='Biblioteca Espectral CONAE',
                           user=user,
                           form=form,
                           posts=posts)


# Vista de Documentos
@app.route('/docs')
def documents():
    docs = sorted(os.listdir(DOCUMENTS_FOLDER))
    detalles = detalle_archivos(docs, DOCUMENTS_FOLDER)
    return render_template('docs.html', list=docs, folder='/docs', detalles=detalles)

# Vista de Documentos
@app.route('/fichas')
def fichas():
    docs = sorted(os.listdir(FICHAS_FOLDER))
    detalles = detalle_archivos(docs, FICHAS_FOLDER)
    return render_template('docs.html', list=docs, folder='/fichas', detalles=detalles)

# Vista de Documentos
@app.route('/protocolos')
def protocolos():
    docs = sorted(os.listdir(PROTOCOLOS_FOLDER))
    detalles = detalle_archivos(docs, PROTOCOLOS_FOLDER)
    return render_template('docs.html', list=docs, folder='/protocolos', detalles=detalles)

# Muestra de documentos online
@app.route('/<folder>/<filename>')
def show_file(folder, filename):
    url = ''
    if folder == 'docs':
        url = DOCUMENTS_FOLDER
    if folder == 'fichas':
        url = FICHAS_FOLDER
    if folder == 'protocolos':
        url = PROTOCOLOS_FOLDER
    return send_from_directory(url, str(filename))


# Vista de Resultados
def resultado(campañas, criterios):
    archivos = os.listdir(CAMPAIGNS_FOLDER)
    lista = []
    for c in campañas:
        for a in archivos:
            if a.find(c.split('-')[1]) > -1:
                lista.append(a)
    return render_template('resultado.html', list=lista, criterios=criterios)


# Muestra archivo de campaña
@app.route('/resultado/<filename>')
def show_campaign(filename):
    d = Descarga()  # Registrar la descarga
    d.agregar(g.user.email, CAMPAIGNS_FOLDER, filename)
    return send_from_directory(CAMPAIGNS_FOLDER, str(filename))


# Carga de Localidades nuevas
@app.route('/cargar/localidad', methods=['GET', 'POST'])
@login_required
def localidad():
    locs = Localidad.query.order_by(Localidad.nombre).all()
    if request.method == 'POST':
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        name = request.form.get('name')
        uname = utf_to_ascii(name.encode('utf-8').decode('utf-8').upper())
        loc = Localidad().agregar(lat=lat, lng=lng, nombre=uname)
        if loc is True:
            return jsonify(json.loads('{"info":"Se agregado la localidad", "loc":"'+str(name)+'"}'))
        if loc == 'Ya existe':
            return jsonify(json.loads('{"info":"La localidad ya existe", "loc":"'+str(name)+'"}'))
        else:
            return jsonify(json.loads('{"error":"No se ha podido agregar"}'))
    return render_template('localidad.html', locs=locs)


# Carga de Metodologias Nuevas
@app.route('/cargar/metodologia', methods=['GET', 'POST'])
@app.route('/cargar/metodologia/<int:page>', methods=['GET', 'POST'])
@login_required
def metodologia(page=1):
    form = MetodologiaForm()
    metods = Metodologia.query.order_by(Metodologia.nombre).paginate(page, POST_PER_PAGE, False)
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            m = Metodologia()
            if m.agregar(form):
                flash('Metodología guardada.', 'success')
            else:
                print('Error')
    return render_template('metod_form.html', form=form, metods=metods, panel=panel)

# Borrar una metodologia existente
@app.route('/cargar/metodologia/borrar/<int:id>')
@login_required
def borrar_metod(id):
    metod = Metodologia.query.get(id)
    if metod is None:
        flash('No se ha podido eliminar la metodologia', 'error')
        return redirect(url_for('metodologia'))
    metod.deleted = True
    db.session.add(metod)
    db.session.commit()
    flash(gettext('La metodología ha sido borrada.'), 'success')
    return redirect(url_for('metodologia'))


# Carga de Proyectos Nuevos
@app.route('/cargar/proyecto', methods=['GET', 'POST'])
@app.route('/cargar/proyecto/<int:page>', methods=['GET', 'POST'])
@login_required
def proyecto(page=1):
    form = ProyectoForm()
    proyectos = Proyecto.query.filter_by(deleted=False).order_by(Proyecto.nombre).paginate(page, POST_PER_PAGE, False)
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            p = Proyecto()
            if p.agregar(form):
                flash('Proyecto guardado.', 'success')
            else:
                print('Error')
    return render_template('proyecto_form.html', form=form, proyectos=proyectos, panel=panel)

# Borrar un proyecto existente
@app.route('/cargar/proyecto/borrar/<int:id>')
@login_required
def borrar_proyecto(id):
    proyecto = Proyecto.query.get(id)
    if proyecto is None:
        flash('No se ha podido eliminar el Proyecto', 'error')
        return redirect(url_for('proyecto'))
    proyecto.deleted = True
    db.session.add(proyecto)
    db.session.commit()
    flash(gettext('El Proyecto ha sido borrado.'), 'success')
    return redirect(url_for('proyecto'))


# Carga de Tipos de Coberturas Nuevas
@app.route('/cargar/tp', methods=['GET', 'POST'])
@login_required
def tp():
    form = TPForm()
    tps = TipoCobertura.query.filter_by(deleted=False).order_by('nombre').all()
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            tp = TipoCobertura()
            if tp.agregar(form):
                flash('Tipo de cobertura guardada.', 'success')
            else:
                print('Error')
    return render_template('tp_form.html', form=form, tps=tps, panel=panel)

# Borrar un tipo de cobertura existente
@app.route('/cargar/tp/borrar/<int:id>')
@login_required
def borrar_tp(id):
    tp = TipoCobertura.query.get(id)
    if tp is None:
        flash('No se ha podido eliminar el tipo de Cobertura', 'error')
        return redirect(url_for('tp'))
    tp.deleted = True
    db.session.add(tp)
    db.session.commit()
    flash(gettext('El Tipo de Cobertura ha sido borrado.'), 'success')
    return redirect(url_for('tp'))


# Carga de Coberturas Nuevas
@app.route('/cargar/cobertura', methods=['GET', 'POST'])
@app.route('/cargar/cobertura/<int:page>', methods=['GET', 'POST'])
@login_required
def cobertura(page=1):
    form = CobForm()
    coberturas = Cobertura.query.filter_by(deleted=False).order_by(Cobertura.nombre).paginate(page, POST_PER_PAGE, False)
    form.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.filter_by(deleted=False).order_by('nombre')]
    form.tipo_cobertura.choices.insert(0, (0, ''))
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            cob = Cobertura()
            if cob.agregar(form):
                flash('Cobertura guardada.', 'success')
            else:
                print('Error')
    return render_template('cobertura_form.html', form=form, coberturas=coberturas, panel=panel)

# Borrar una cobertura existente
@app.route('/cargar/cobertura/borrar/<int:id>')
@login_required
def borrar_cobertura(id):
    cob = Cobertura.query.get(id)
    if cob is None:
        flash('No se ha podido eliminar la Cobertura', 'error')
        return redirect(url_for('cobertura'))
    cob.deleted = True
    db.session.add(cob)
    db.session.commit()
    flash(gettext('La Cobertura ha sido borrada.'), 'success')
    return redirect(url_for('cobertura'))


# Carga de Radiometros Nuevos
@app.route('/cargar/radiometro', methods=['GET', 'POST'])
@login_required
def radiometro():
    form = RadiometroForm()
    radiometros = Radiometro.query.filter_by(deleted=False).order_by(Radiometro.nombre).all()
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            rad = Radiometro()
            if rad.agregar(form):
                flash('Espectro-radiómetro guardado.', 'success')
            else:
                print('Error')
    return render_template('radiometro_form.html', form=form, radiometros=radiometros, panel=panel)


# Borrar un radiometro existente
@app.route('/cargar/radiometro/borrar/<int:id>')
@login_required
def borrar_radiometro(id):
    rad = Radiometro.query.get(id)
    if rad is None:
        flash('No se ha podido eliminar el Espectro-radiómerto', 'error')
        return redirect(url_for('radiometro'))
    rad.deleted = True
    db.session.add(rad)
    db.session.commit()
    flash(gettext('El Espectro-radiómetro ha sido borrado.'), 'success')
    return redirect(url_for('radiometro'))


# Carga de Espectralones Nuevos
@app.route('/cargar/patron', methods=['GET', 'POST'])
@login_required
def patron():
    form = PatronForm()
    patrones = Patron.query.filter_by(deleted=False).order_by(Patron.nombre).all()
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            patron = Patron()
            if patron.agregar(form):
                flash('Patrón guardado.', 'success')
            else:
                print('Error')
    return render_template('patron_form.html', form=form, patrones=patrones, panel=panel)

# Borrar un Espectralon existente
@app.route('/cargar/patron/borrar/<int:id>')
@login_required
def borrar_patron(id):
    patron = Patron.query.get(id)
    if patron is None:
        flash('No se ha podido eliminar el Patrón', 'error')
        return redirect(url_for('patron'))
    patron.deleted = True
    db.session.add(patron)
    db.session.commit()
    flash(gettext('El Patrón ha sido borrado.'), 'success')
    return redirect(url_for('patron'))


# Carga de Fotometros Nuevos
@app.route('/cargar/fotometro', methods=['GET', 'POST'])
@login_required
def fotometro():
    form = FotometroForm()
    fotometros = Fotometro.query.filter_by(deleted=False).order_by(Fotometro.nombre).all()
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            fotometro = Fotometro()
            if fotometro.agregar(form):
                flash('Fotómetro guardado.', 'success')
            else:
                print('Error')
    return render_template('fotometro_form.html', form=form, fotometros=fotometros, panel=panel)

# Borrar un Fotometro existente
@app.route('/cargar/fotometro/borrar/<int:id>')
@login_required
def borrar_fotometro(id):
    fotometro = Fotometro.query.get(id)
    if fotometro is None:
        flash('No se ha podido eliminar el Fotómetro', 'error')
        return redirect(url_for('fotometro'))
    fotometro.deleted = True
    db.session.add(fotometro)
    db.session.commit()
    flash(gettext('El Fotómetro ha sido borrado.'), 'success')
    return redirect(url_for('fotometro'))


# Carga de Camaras Nuevas
@app.route('/cargar/camara', methods=['GET', 'POST'])
@login_required
def camara():
    form = CamaraForm()
    camaras = Camara.query.filter_by(deleted=False).order_by(Camara.nombre).all()
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            camara = Camara()
            if camara.agregar(form):
                flash('Cámara guardada.', 'success')
            else:
                print('Error')
    return render_template('camara_form.html', form=form, camaras=camaras, panel=panel)

# Borrar una Cámara existente
@app.route('/cargar/camara/borrar/<int:id>')
@login_required
def borrar_camara(id):
    camara = Camara.query.get(id)
    if camara is None:
        flash('No se ha podido eliminar la Cámara', 'error')
        return redirect(url_for('camara'))
    camara.deleted = True
    db.session.add(camara)
    db.session.commit()
    flash(gettext('La Cámara ha sido borrada.'), 'success')
    return redirect(url_for('camara'))


# Carga de GPS Nuevos
@app.route('/cargar/gps', methods=['GET', 'POST'])
@login_required
def gps():
    form = GPSForm()
    gpses = Gps.query.filter_by(deleted=False).order_by(Gps.nombre).all()
    if request.args.get('c') == 'n':
        panel = 'none'
    else:
        panel = 'block'
    if request.method == 'POST':
        if form.validate_on_submit():
            gps = Gps()
            if gps.agregar(form):
                flash('GPS guardado.', 'success')
            else:
                print('Error')
    return render_template('gps_form.html', form=form, gpses=gpses, panel=panel)

# Borrar un Fotometro existente
@app.route('/cargar/gps/borrar/<int:id>')
@login_required
def borrar_gps(id):
    gps = Gps.query.get(id)
    if gps is None:
        flash('No se ha podido eliminar el GPS', 'error')
        return redirect(url_for('gps'))
    gps.deleted = True
    db.session.add(gps)
    db.session.commit()
    flash(gettext('El GPS ha sido borrado.'), 'success')
    return redirect(url_for('gps'))

# Pagina de Contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    if request.method == 'POST':
        response = request.form.get('g-recaptcha-response')
        if checkRecaptcha(response, SECRET_KEY_CAPTCHA):
            if form.validate_on_submit():
                contact_notification(form)
                flash('Su mensaje ha sido enviado.\nEn breve nos comunicaremos.\nGracias por contactarse', 'success')
        else:
            flash('Indique que No es un robot', 'error')
    return render_template('contacto.html', form=form, siteKey=SITE_KEY_CAPTCHA)
