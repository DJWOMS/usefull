from rest_framework import serializers
from src.profiles.serializers import ProfileSerializer
from .models import Follower


class FollowerListSerializer(serializers.ModelSerializer):
    """ Followers list """
    subscriber = ProfileSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ('subscriber',)


class FollowingListSerializer(serializers.ModelSerializer):
    """ Following list """
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ('user',)

