"""
WSGI config for optifino project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from optifino.fastapi_app import create_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optifino.settings')

application = get_wsgi_application()

app = create_application(application)
