#!virtual/bin/python
__author__ = 'Juanjo'

import os, sys

if sys.platform == 'win32':
    pybabel = 'virtual\\Scripts\\pybabel'
else:
    pybabel = 'virtual/bin/pybabel'

os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system(pybabel + ' update -i messages.pot -d app/translations')
os.unlink('messages.pot')
