# -*- coding: utf-8 -*-

from datetime import datetime
import os
import re
import requests
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import get_debug_queries
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import gettext
from app import app, db, lm, oid, babel
from .emails import follower_notification, error_notification
from .forms import LoginForm, EditForm, PostForm, SearchForm, ConsultarForm, ArchivoForm, LoginConaeForm, NuevaCoberturaForm
from .models import User, Post, Localidad, TipoCobertura, Cobertura, Campania, Proyecto, \
    Muestra
from .translate import microsoft_translate
from .utils import cargar_archivo, ini_consulta_camp, ini_editar_form, ini_nuevo_form
from config import POST_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, UPLOAD_FOLDER, DOCUMENTS_FOLDER, LOGOUT, \
    CAMPAIGNS_FOLDER, DATABASE_QUERY_TIMEOUT
from guess_language import guessLanguage
from .oauth import OAuthSignIn, ConaeSignIn


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
    form = LoginConaeForm()
    conae_sign = ConaeSignIn()
    if request.method == 'POST':
        if form.validate_on_submit():
            datos = conae_sign.login(form)
            if datos:
                conae_after_login(datos)
            else:
                return redirect(url_for('login'))
        else:
            flash('Falta Completar:', 'error')
    return render_template('login.html',
                           form=form)



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
        nickname = datos['nombre']+' '+datos['apellido']# Se intenta obtener el nickname de la respuesta.
        if nickname is None or nickname == "":          # Si no se obtiene de la respuesta "resp",
            nickname = datos['email'].split('@')[0]     # se entresaca el nickname desde el email hasta el '@'
        nickname = User.make_valid_nickname(nickname)   # Validaciones previas a la aceptacion del nickname.
        nickname = User.make_unique_nickname(nickname)  # No aceptar duplicados.
        user = User(social_id='sinredsocial', nickname=nickname, email=datos['email'])# Obtenidos los datos, creamos User con el nickname y email
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
@oid.after_login
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
        requests.get(LOGOUT + session['userid'])
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
    if user == None:                                    # Si no existe el usuario,
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
    form = EditForm(g.user.nickname)   # Cargamos un formulario del tipo EditForm
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


# Carga de archivos paso 1
@app.route('/cargar/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    form_n = ini_nuevo_form()
    archivoform = ArchivoForm()
    if request.method == 'POST':
        if form_n.validate_on_submit():
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
                flash('No ingresó ningún archivo de Radiancia', 'error')
            if count_radavg == 0:
                flash('No ingresó ningún archivo de Radiancia Promedio', 'error')
            if count_radstd == 0:
                flash('No ingresó ningún archivo de Radiancia Desviación Estándar', 'error')
            if count_ref == 0:
                flash('No ingresó ningún archivo de Reflectancia', 'error')
            if count_refavg == 0:
                flash('No ingresó ningún archivo de Reflectancia Promedio', 'error')
            if count_refstd == 0:
                flash('No ingresó ningún archivo de Reflectancia Desviación Estándar', 'error')
            if count_img == 0:
                flash('No ingresó ningún archivo de Imagen', 'error')
            if count_rad>0 and count_radavg>0 and count_radstd>0 and count_ref>0 and count_refavg>0 and count_refstd>0 and form_n.validate_on_submit():
                render_template('resultado.html')
        else:
            flash('Falta Completar:', 'error')
    return render_template('cargar_n.html',
                           form_n=form_n,
                           archivoform=archivoform)


@app.route('/cargar/editar', methods=['GET', 'POST'])
@login_required
def editar_consulta():
    id = request.args.get('id', 0, type=int)
    form_c = ini_consulta_camp()
    form_e = ini_editar_form(id)
    form_nc = NuevaCoberturaForm()
    archivoform = ArchivoForm()
    if request.method == 'POST':
        if form_c.validate_on_submit():
            id = form_c.ccampania.data
            form_e = ini_editar_form(id)
        else:
            flash('Falta Completar:', 'error')
            return render_template('cargar_e.html',
                                   form_c=form_c,
                                   form_nc=form_nc,
                                   form_e=form_e,
                                   archivoform=archivoform)
    return render_template('cargar_e.html',
                           form_c=form_c,
                           form_nc=form_nc,
                           form_e=form_e,
                           archivoform=archivoform)


@app.route('/editar/nueva_cobertura', methods=['GET', 'POST'])
@login_required
def nueva_cobertura():
    form = NuevaCoberturaForm()
    if request.method == 'POST':
        nombre = form.ncnombre.data
        id_tipocobertura = int(form.ncid_tipocobertura.data)
        altura = float(form.ncaltura.data)
        fenologia = form.ncfenologia.data
        observaciones = request.form.getlist('ncobservaciones[]')
        try:
            cob = Cobertura(nombre=nombre,
                            id_tipocobertura=id_tipocobertura,
                            altura=altura,
                            fenologia=fenologia,
                            observaciones=observaciones)
            db.session.add(cob)
            db.session.commit()
            return jsonify({'cob': cob.nombre})
        except:
            db.session.rollback()
            return jsonify({'cob': 'error',
                            'error': 'Datos invalidos.'})
        return jsonify({'cob': 'error',
                        'error': form.errors})
    return render_template('nc_form.html', form=form)


@app.route('/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    form_e = ini_editar_form(id)
    archivoform = ArchivoForm()
    if request.method == 'POST':
        if form_e.validate_on_submit():
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
                flash('No ingresó ningún archivo de Radiancia', 'error')
            if count_radavg == 0:
                flash('No ingresó ningún archivo de Radiancia Promedio', 'error')
            if count_radstd == 0:
                flash('No ingresó ningún archivo de Radiancia Desviación Estándar', 'error')
            if count_ref == 0:
                flash('No ingresó ningún archivo de Reflectancia', 'error')
            if count_refavg == 0:
                flash('No ingresó ningún archivo de Reflectancia Promedio', 'error')
            if count_refstd == 0:
                flash('No ingresó ningún archivo de Reflectancia Desviación Estándar', 'error')
            if count_img == 0:
                flash('No ingresó ningún archivo de Imagen', 'error')
            if count_rad>0 and count_radavg>0 and count_radstd>0 and count_ref>0 and count_refavg>0 and count_refstd>0 and form_e.validate_on_submit():
                render_template('resultado.html')
        if not form_e.validate_on_submit():
            flash('Falta Completar:', 'error')
        return render_template('cargar_e.html',
                               form_e=form_e,
                               archivoform=archivoform)
    return render_template('cargar_e.html',
                           form_e=form_e,
                           archivoform=archivoform)


# Carga de archivos
@app.route('/consultar', methods=['GET', 'POST'])
@login_required
def consultar():
    form = ConsultarForm()
    form.proyecto.choices = [(p.id, p.nombre) for p in Proyecto.query.order_by('nombre')]
    form.proyecto.choices.insert(0, (0, ''))
    form.cobertura.choices = [(cob.id, cob.nombre) for cob in Cobertura.query.order_by('nombre')]
    form.cobertura.choices.insert(0, (0, ''))
    form.localidad.choices = [(l.id, l.nombre) for l in Localidad.query.order_by('nombre')]
    form.localidad.choices.insert(0, (0, ''))
    form.tipo_cobertura.choices = [(tp.id, tp.nombre) for tp in TipoCobertura.query.order_by('nombre')]
    form.tipo_cobertura.choices.insert(0, (0, ''))
    if request.method == 'POST':
        proy = form.proyecto.data
        loc = form.localidad.data
        cob = form.cobertura.data
        tp = form.tipo_cobertura.data
        fi = form.fecha_inicio.data
        ff = form.fecha_fin.data
        camps = []
        criterios = {}
        if loc == 0 and proy == 0 and cob == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.all()
        if loc > 0 and proy == 0 and cob == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.filter(Campania.id_localidad == loc).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
        if loc > 0 and fi is not None and ff is not None and proy == 0 and cob == 0 and tp == 0:
            camps = Campania.query.filter(Campania.id_localidad == loc, Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if loc > 0 and tp > 0 and proy == 0 and cob == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   Cobertura.id_tipocobertura == tp).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
        if loc > 0 and cob > 0 and proy == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra).filter(Campania.id_localidad == loc, Muestra.id_cobertura == cob).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if proy > 0 and loc == 0 and cob == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.filter(Campania.id_proyecto == proy).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
        if proy > 0 and loc > 0 and cob == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.filter(Campania.id_proyecto == proy, Campania.id_localidad == loc).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
        if proy > 0 and fi is not None and ff is not None and loc == 0 and cob == 0 and tp == 0:
            camps = Campania.query.filter(Campania.id_proyecto == proy, Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if proy > 0 and cob > 0 and loc == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra).filter(Campania.id_proyecto == proy, Muestra.id_cobertura == cob).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if proy > 0 and tp > 0 and loc == 0 and cob == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_proyecto == proy,
                                                                   Cobertura.id_tipocobertura == tp).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
        if fi is not None and loc == 0 and proy == 0 and tp == 0 and cob == 0 and ff is None:
            camps = Campania.query.filter(Campania.fecha >= fi).all()
            criterios['Fecha Inicio'] = fi
        if ff is not None and loc == 0 and cob == 0 and tp == 0 and fi is None and proy == 0:
            camps = Campania.query.filter(Campania.fecha <= ff).all()
            criterios['Fecha Fin'] = ff
        if fi is not None and ff is not None and cob == 0 and tp == 0 and proy == 0 and loc == 0:
            camps = Campania.query.filter(Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if cob > 0 and loc == 0 and proy == 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra).filter(Muestra.id_cobertura == cob).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if cob > 0 and fi is not None and ff is not None and loc == 0 and proy == 0 and tp == 0:
            camps = Campania.query.join(Muestra).filter(Campania.fecha >= fi, Campania.fecha <= ff,
                                                        Muestra.id_cobertura == cob).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if tp > 0 and loc == 0 and proy == 0 and cob == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Cobertura.id_tipocobertura == tp).all()
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
        if tp > 0 and fi is not None and ff is not None and loc == 0 and proy == 0 and cob == 0:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.fecha >= fi, Campania.fecha <= ff,
                                                                   Cobertura.id_tipocobertura == tp).all()
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if tp > 0 and cob > 0 and proy == 0 and loc == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if tp > 0 and cob > 0 and proy > 0 and loc == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_proyecto == proy,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
        if tp > 0 and cob > 0 and loc > 0 and proy == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if tp > 0 and loc > 0 and fi is not None and ff is not None and cob == 0 and proy == 0:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if tp > 0 and cob > 0 and fi is not None and ff is not None and loc == 0 and proy == 0:
            camps = Campania.query.join(Muestra, Cobertura).filter(Muestra.id_cobertura == cob,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if loc > 0 and cob > 0 and fi is not None and ff is not None and tp == 0 and proy == 0:
            camps = Campania.query.join(Muestra).filter(Muestra.id_cobertura == cob, Campania.id_localidad == loc,
                                                        Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if proy > 0 and loc > 0 and fi is not None and ff is not None and cob == 0 and tp == 0:
            camps = Campania.query.filter(Campania.id_proyecto == proy, Campania.id_localidad == loc,
                                          Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if proy > 0 and cob > 0 and fi is not None and ff is not None and loc == 0 and tp == 0:
            camps = Campania.query.join(Muestra).filter(Muestra.id_cobertura == cob, Campania.id_proyecto == proy,
                                                        Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if proy > 0 and loc > 0 and tp > 0 and cob == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_proyecto == proy,
                                                                   Campania.id_localidad == loc,
                                                                   Cobertura.id_tipocobertura == tp).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
        if tp > 0 and proy > 0 and fi is not None and ff is not None and loc == 0 and cob == 0:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_proyecto == proy,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Campania.fecha >= fi, Campania.fecha <= ff).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
        if proy > 0 and loc > 0 and cob > 0 and tp == 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra).filter(Campania.id_proyecto == proy, Campania.id_localidad == loc,
                                                        Muestra.id_cobertura == cob).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if tp > 0 and cob > 0 and proy > 0 and loc > 0 and fi is None and ff is None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_proyecto == proy,
                                                                   Campania.id_localidad == loc,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        if tp > 0 and cob > 0 and proy > 0 and loc > 0 and fi is not None and ff is not None:
            camps = Campania.query.join(Muestra, Cobertura).filter(Campania.id_localidad == loc,
                                                                   Campania.id_proyecto == proy,
                                                                   Campania.fecha >= fi,
                                                                   Campania.fecha <= ff,
                                                                   Cobertura.id_tipocobertura == tp,
                                                                   Muestra.id_cobertura == cob).all()
            criterios['Localidad'] = Localidad.query.filter_by(id=loc).first().nombre
            criterios['Proyecto'] = Proyecto.query.filter_by(id=proy).first().nombre
            criterios['Fecha Inicio'] = fi
            criterios['Fecha Fin'] = ff
            criterios['Tipo Cobertura'] = TipoCobertura.query.filter_by(id=tp).first().nombre
            criterios['Cobertura'] = Cobertura.query.filter_by(id=cob).first().nombre
        nombres = []
        for c in camps:
            nombres.append(c.nombre)
        return resultado(nombres, criterios)
    return render_template('consultar.html', form=form)


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
@login_required
def documents():
    docs = os.listdir(DOCUMENTS_FOLDER)
    return render_template('docs.html', list=docs)


# Muestra de documentos online
@app.route('/docs/<filename>')
def show_file(filename):
    return send_from_directory(DOCUMENTS_FOLDER, filename)


# Vista de Resultados
@login_required
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
    return send_from_directory(CAMPAIGNS_FOLDER, filename)



