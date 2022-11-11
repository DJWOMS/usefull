from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Profile, Technology, ColorSchema
from .services.service import delete_old_file, validate_size_image
from ..achievements.serializers import AchievementSerializer
from ..followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """ Profile serializer for another serializer """

    class Meta:
        model = Profile
        fields = ('id', 'username', 'avatar', 'github')


class TechnologyListSerializer(serializers.ModelSerializer):
    """ Technology serializer """
    class Meta:
        model = Technology
        fields = ('id', 'name')


class GetProfileSerializer(serializers.ModelSerializer):
    """ Вывод инфо о user """
    # avatar = serializers.ImageField(read_only=True)
    technology = TechnologyListSerializer(read_only=False, many=True)
    achievement = AchievementSerializer(read_only=True, many=True)
    github = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        technologies = validated_data.pop('technology')
        instance = super().update(instance, validated_data)
        instance.technology.clear()
        for technology in technologies:
            new_technology = get_object_or_404(Technology, name=technology.get('name'))

            if instance.technology.count() < 10:
                instance.technology.add(new_technology)
        return instance

    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "bio",
            "github",
            "birthday",
            "gender",
            "technology",
            "achievement",
            "subscribers_count",
            "subscription_count"
        )


class GetProfileAvatarSerializer(serializers.ModelSerializer):
    """ Вывод аватара пользователя """

    class Meta:
        model = Profile
        fields = ("avatar",)

    def update(self, instance, validated_data):
        validate_size_image(validated_data.get("avatar"))
        if instance.avatar:
            delete_old_file(instance.avatar.path)
        return super().update(instance, validated_data)


class GetProfilePublicSerializer(serializers.ModelSerializer):
    """ Вывод публичной инфы о user """
    technology = TechnologyListSerializer(read_only=True, many=True)
    achievement = AchievementSerializer(read_only=True, many=True)
    is_follow = serializers.SerializerMethodField('get_is_follow')

    def get_is_follow(self, obj):
        return Follower.objects.filter(subscriber=self.context['request'].user, user=obj).exists()

    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "bio",
            "github",
            "birthday",
            "gender",
            "technology",
            "achievement",
            "subscribers_count",
            "subscription_count",
            "is_follow"
        )


class ProgressSerializer(serializers.Serializer):
    course_signup_count = serializers.IntegerField()
    lesson_success = serializers.IntegerField()
    lesson_non_success = serializers.IntegerField()
    task_count = serializers.IntegerField()
    task_success_count = serializers.IntegerField()


class ColorSchemaSerializer(serializers.ModelSerializer):
    """ Serializer of color scheme
    """

    class Meta:
        model = ColorSchema
        fields = ("theme", "scheme", "layout")
