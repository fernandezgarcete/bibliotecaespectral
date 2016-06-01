#!virtual\Script\python
# -*- coding: utf-8 -*-
__author__ = 'Juanjo'

from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app


app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
app.run(debug=True)
