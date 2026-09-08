"""ASGI config for chore_master project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chore_master.settings")

application = get_asgi_application()
