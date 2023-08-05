"""WSGI config for ``jwql`` project.

It exposes the WSGI callable as a module-level variable named
``application``.

References
----------

    For more information on this file, see:
        ``https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/``
"""

import os

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jwql_proj.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jwql.website.jwql_proj.settings")

application = get_wsgi_application()
