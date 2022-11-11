from abc import ABC

from rest_framework import serializers

from .models import Room, Message
from ..base.serializers import ModelSerializer
from ..profiles.serializers import ProfileSerializer
from ..team.models import TeamMember


class CreateRoomSerializer(serializers.Serializer):
    """Сериализация создания комнаты чата"""
    member = serializers.IntegerField()

    class Meta:
        fields = ("id", "member")


class RoomSerializer(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    member = ProfileSerializer(many=True)

    class Meta:
        model = Room
        fields = ("id", "name", "user", "member", "team", "create_date")


class CreateRoomTeamSerializer(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    class Meta:
        model = Room
        fields = ("id", "team")

    def create(self, validated_data):
        _team = validated_data.get('team')
        instance = Room.objects.create(**validated_data)
        instance.member.add(*TeamMember.objects.filter(team=_team))
        return instance


class MessageSerializer(ModelSerializer):
    """Сериализация чата"""
    user = ProfileSerializer()

    class Meta:
        model = Message
        fields = ("user", "text", "create_date")


class MessagePostSerializer(serializers.ModelSerializer):
    """Сериализация создания сообщения"""

    class Meta:
        model = Message
        fields = ("room", "text")


class MessageChatSerializer(serializers.ModelSerializer):
    get_create_date = serializers.SerializerMethodField()
    user = ProfileSerializer()

    class Meta:
        model = Message
        exclude = []
        #depth = 1

    def get_create_date(self, obj: Message):
        return obj.create_date.strftime("%d-%m-%Y %H:%M:%S")


class RoomChatSerializer(serializers.ModelSerializer):
    messages = MessageChatSerializer(many=True, read_only=True)
    member = ProfileSerializer(many=True)

    class Meta:
        model = Room
        fields = ["pk", "name", "user", "team", "messages", "member"]
        #depth = 1
        read_only_fields = ["messages"]
