"""WSGI config for chore_master project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chore_master.settings")

application = get_wsgi_application()
