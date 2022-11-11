from rest_framework import serializers

from src.profiles.models import Profile
from src.profiles.serializers import ProfileSerializer


class FilterCommentListSerializer(serializers.ListSerializer):
    """ Фильтр комментариев, только parents """

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ModelSerializer(serializers.ModelSerializer):
    """ Serializer for all serializer where is user """
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        try:
            user = Profile.objects.get(id=obj.user)
        except:
            return obj.user
        else:
            return ProfileSerializer(user).data
