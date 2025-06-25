"""
ASGI config for techsupport project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from dotenv import load_dotenv


load_dotenv()

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 
    os.getenv('DJANGO_SETTINGS_MODULE', 'techsupport.settings.dev')
)

django.setup()

from techsupport.middleware import JWTWebSocketAuthMiddleware
from notifications.urls import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTWebSocketAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
