import os, os.path, sys
site_root = os.path.dirname(os.path.dirname(__file__))
root = os.path.dirname(site_root)
sys.path.insert(0, root)
sys.path.insert(0, os.path.join(root, 'venv', 'lib', 'python%s.%s'%(sys.version_info[0], sys.version_info[1]), 'site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'smgsite.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/www/.python-eggs'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

