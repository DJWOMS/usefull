from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status

from . import serializers
from .services import create_room
from ..base.permissions import IsMemberOfRoom, IsAuthorOfTeam
from .models import Room, Message


def index(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name:
            room = Room.objects.create(name=name, user_id=47)
            room.member.add(47)
            print(room.pk)
            HttpResponseRedirect(reverse("room", kwargs={"pk": room.pk}))
    return render(request, 'chat/index.html')


def room(request, pk):
    return render(request, 'chat/room.html', {"room": pk})


class RoomView(viewsets.ModelViewSet):
    """Список диалогов с юзерами"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(member=self.request.user)

    @action(detail=False, serializer_class=serializers.CreateRoomSerializer, methods=['post'])
    def create_room(self, request):
        serializer = serializers.CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            create_room(request)
            return Response(status=201)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        serializer_class=serializers.CreateRoomTeamSerializer,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated, IsAuthorOfTeam]
    )
    def create_team_room(self, request):
        serializer = serializers.CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=201)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DialogView(APIView):
    """Диалог чата, сообщение"""
    permission_classes = [permissions.IsAuthenticated, IsMemberOfRoom]

    def get(self, request, *args, **kwargs):
        room = kwargs['pk']
        chat = Message.objects.filter(room=room).order_by('create_date')

        paginator = Paginator(chat, 20)
        page = request.GET.get('page')
        try:
            chat = paginator.page(page)
        except PageNotAnInteger:
            chat = paginator.page(1)
        except EmptyPage:
            chat = paginator.page(paginator.num_pages)

        serializer = serializers.MessageSerializer(chat, many=True)

        return Response(serializer.data, status=200)

    def post(self, request):
        dialog = serializers.MessagePostSerializer(data=request.data)

        if dialog.is_valid():
            dialog.save(user=request.user)
            return Response(dialog.data, status=201)
        else:
            return Response(status=400)
