#!virtual/bin/python
__author__ = 'Juanjo'

import os, sys

if sys.platform == 'win32':
    pybabel = 'virtual\\Scripts\\pybabel'
else:
    pybabel = 'virtual/bin/pybabel'

os.system(pybabel + ' compile -d app/translations')
