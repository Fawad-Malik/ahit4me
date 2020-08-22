"""
WSGI config for applai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from load_env import read_env

read_env()

try:
    import newrelic.agent
    newrelic.agent.initialize(os.path.abspath('newrelic.ini'))
except ImportError:
    pass


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iow.settings")

application = get_wsgi_application()
