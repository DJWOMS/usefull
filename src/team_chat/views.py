from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import requests


class RoomListView(APIView):
    """Team room list view """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(status=200)


class DialogView(APIView):
    """Chatting"""
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # messages = gitter.get(gitter.set_message_url(find_by_room_id(gitter, **kwargs)))
        # messages = gitter.get_messages(**kwargs)
        # response = gitter.stream_get(
        #     gitter.set_message_url(find_by_room_id(gitter, **kwargs)),
        #     **kwargs
        # )
        # for stream_messages in response.iter_lines():
        #     if stream_messages:
        #         print(stream_messages)
        return Response(status=200)

    def post(self, request, *args, **kwargs):
        # message = gitter.send_message(request, **kwargs)
        return Response(status=200)
