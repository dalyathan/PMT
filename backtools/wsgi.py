"""
WSGI config for backtools project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backtools.settings')
os.environ.setdefault('PYTHONPATH','/usr/local/lib/python3.8/site-packages')

application = get_wsgi_application()
