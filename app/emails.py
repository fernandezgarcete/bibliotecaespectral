# -*- coding: utf-8 -*-

__author__ = 'Juanjo'

from flask.ext.mail import Message
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
def send_email(subj, sender, recip, text_body, html_body):
    msg = Message(subj, sender=sender, recipients=recip)
    msg.body = text_body
    msg.html = html_body
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

