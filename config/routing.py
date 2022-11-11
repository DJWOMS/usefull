from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from src.chat.authmiddleware import TokenAuthMiddleware
from src.chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
