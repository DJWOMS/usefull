from rest_framework import serializers

from ..base.serializers import FilterCommentListSerializer, ModelSerializer
from .models import Post, Comment, Team, TeamMember, Invitation, SocialLink
from ..profiles.serializers import ProfileSerializer
from ..profiles.services.service import delete_old_file, validate_size_image


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        exclude = ()


class InvitationListSerializer(ModelSerializer):
    """Invitation list serializer"""
    user = ProfileSerializer()
    team = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Invitation
        fields = ("id", "team", "user", "asking", "create_date")


class InvitationSerializer(serializers.ModelSerializer):
    """Invitation detail serializer"""

    class Meta:
        model = Invitation
        fields = ("id", "team", "user", "create_date")


class InvitationAskingSerializer(serializers.ModelSerializer):
    """Invitation detail serializer"""

    class Meta:
        model = Invitation
        fields = ("id", "team", "create_date")


class AcceptInvitationSerializer(serializers.ModelSerializer):
    """Accepted invitation serializer"""
    class Meta:
        model = Invitation
        fields = ("accepted",)


class TeamMemberSerializer(serializers.ModelSerializer):
    """TeamMember serializer"""
    user = ProfileSerializer()

    class Meta:
        model = TeamMember
        fields = ("team", "user",)


class TeamSerializer(serializers.ModelSerializer):
    """Team detail serializer"""
    user = ProfileSerializer(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    is_send_invitation_asking = serializers.SerializerMethodField(read_only=True)
    social_links = SocialLinkSerializer(many=True, read_only=True)

    def get_is_send_invitation_asking(self, obj):
        return Invitation.objects.filter(team=obj, user=self.context['request'].user, asking=True).exists()

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "tagline",
            "user",
            "avatar",
            "members",
            "is_send_invitation_asking",
            "social_links"
        )


class TeamCommentCreateSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту """
    class Meta:
        model = Comment
        fields = ("post", "text", "parent")


class TeamCommentChildrenListSerializer(ModelSerializer):
    """ Comment children list serializer"""
    user = ProfileSerializer()

    class Meta:
        model = Comment
        fields = ("id", "user", "text", "create_date")


class TeamCommentListSerializer(ModelSerializer):
    """ Список комментариев """
    user = ProfileSerializer()
    children = TeamCommentChildrenListSerializer(read_only=True, many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "user", "text", "create_date", "children")


class TeamPostSerializer(ModelSerializer):
    """ Вывод и редактирование поста """
    user = ProfileSerializer(read_only=True)
    comments = TeamCommentListSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "team", "user", "create_date", "text", "comments", "view_count")


class TeamListPostSerializer(ModelSerializer):
    """ Список постов """
    user = ProfileSerializer()
    comments = TeamCommentListSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "team",
            "create_date",
            "user",
            "text",
            "view_count",
            "comments",
            "comments_count"
        )


class TeamAvatarSerializer(serializers.ModelSerializer):
    """ Team avatar serializer """
    class Meta:
        model = Team
        fields = ("avatar",)

    def update(self, instance, validated_data):
        validate_size_image(validated_data.get("avatar"))
        if instance.avatar:
            delete_old_file(instance.avatar.path)
        return super().update(instance, validated_data)


class TeamListSerializer(ModelSerializer):
    """Team list serializer"""
    user = ProfileSerializer()
    members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "name", "user", "avatar", "tagline", "members")


class ByUserTeamMemberSerializer(serializers.ModelSerializer):
    """TeamMember serializer"""

    class Meta:
        model = TeamMember
        fields = ("team", "user",)


class ByUserTeamListSerializer(ModelSerializer):
    """By user Team list serializer"""
    members = ByUserTeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "members")
