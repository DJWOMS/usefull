from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/room/', consumers.RoomConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     path('ws/chat/<int:room_name>/', consumers.ChatConsumer.as_asgi()),
# ]
