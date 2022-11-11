from rest_framework import serializers
from .models import Achievement


class AchievementSerializer(serializers.ModelSerializer):
    """ Achievement serializer """
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Achievement
        fields = ("id", "category", "name", "description")
