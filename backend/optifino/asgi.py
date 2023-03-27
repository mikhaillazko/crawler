import os

from django.core.asgi import get_asgi_application

from .fastapi_app import create_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optifino.settings')

application = get_asgi_application()

app = create_application(application)
