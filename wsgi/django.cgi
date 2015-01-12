#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, os, os.path
import wsgiref.handlers

stdout = sys.stdout
sys.stdout = sys.stderr   # manual print statements go to error log

site_root = os.path.dirname(os.path.dirname(__file__))
root = os.path.dirname(site_root)
sys.path.insert(0, root)
sys.path.insert(0, os.path.join(root, 'venv', 'lib', 'python%s.%s'%(sys.version_info[0], sys.version_info[1]), 'site-packages'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'smgsite.settings'

if __name__ == '__main__':
    # Create a Django application for WSGI.
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()
    #print os.environ['LD_LIBRARY_PATH']
    wsgiref.handlers.BaseCGIHandler(sys.stdin, stdout, sys.stderr, os.environ, multithread=False, multiprocess=True).run(application)
