# -*- coding: utf-8 -*-
__author__ = 'Juanjo'

from threading import Thread

# Decorado para funciones asíncronas en segundo plano
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
