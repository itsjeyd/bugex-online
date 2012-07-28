import os
import sys

# redirect print statements to apache log
sys.stdout = sys.stderr

# add python path
path = '/var/django/bugex_online'
if path not in sys.path:
    sys.path.append(path)

# define settings to use
os.environ['DJANGO_SETTINGS_MODULE'] = 'bugex_online.settings'

# register with WSGI handler
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
