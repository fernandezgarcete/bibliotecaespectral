# -*- coding: utf-8 -*-

__author__ = 'Juanjo'

from flask_mail import Message
from flask import render_template
from config import ADMINS
from app import mail, app
from .decorators import async


# Envíos asincronos para procesar en segundo plano
@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Esquema de mail
def send_email(subj, sender, recip, text_body, html_body, attachment):
    msg = Message(subj, sender=sender, recipients=recip)
    if text_body:
        msg.body = text_body
    if html_body:
        msg.html = html_body
    if attachment:
        # attachment es un path a un archivo
        with open(attachment) as f:
            msg.attach(attachment, None, f.read())
    # Enviamos en segundo plano
    send_async_email(app, msg)


# Notificaciones de seguimiento
def follower_notification(followed, follower):
    send_email('[BiblioEspectral] %s ahora te sigue!' % follower.nickname,  # Asunto del mensaje,
               ADMINS[0],                                                   # Remitente
               [followed.email],                                            # Destinatario
               render_template('follower_email.txt',                        # Cuerpo del mensaje en texto plano
                               user=followed, follower=follower),
               render_template('follower_email.hmtl',                       # Cuerpo del mensaje en HTML.
                               user=followed, follower=follower))


def error_notification(user):
    log = '/var/log/apache2/error.log'
    send_email('[BibliotecaEspectral] ERROR 500',       # Asunto
               ADMINS[0],                               # Remitente
               ADMINS[0],                               # Destinatario
               render_template('error_500_email.txt',   # Cuerpo del mail
                               user=user),
               None,                                    # Cuerpo html
               log)                                     # Path archivo adjunto
