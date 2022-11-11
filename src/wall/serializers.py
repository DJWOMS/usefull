from rest_framework import serializers

from ..base.serializers import FilterCommentListSerializer, ModelSerializer
from .models import Post, Comment
from ..profiles.serializers import ProfileSerializer


class WallCommentChildrenListSerializer(ModelSerializer):
    """ Comment children list serializer """
    user = ProfileSerializer()

    class Meta:
        model = Comment
        fields = ("id", "user", "text", "create_date", "parent")


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту """
    id = serializers.IntegerField(read_only=True)
    user = ProfileSerializer(read_only=True)
    children = WallCommentChildrenListSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ("id", "post", "text", "parent", "user", "children", "create_date")


class WallCommentListSerializer(ModelSerializer):
    """ Список комментариев """
    user = ProfileSerializer()
    children = WallCommentChildrenListSerializer(read_only=True, many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "user", "text", "create_date", "children")


class PostSerializer(serializers.ModelSerializer):
    """ Вывод и редактирование поста """
    user = ProfileSerializer(read_only=True)
    wall_comments = WallCommentListSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "create_date", "text", "wall_comments", "view_count")


class ListPostSerializer(ModelSerializer):
    """ Список постов """
    user = ProfileSerializer()
    wall_comments = WallCommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "create_date", "user", "text", "comments_count", "wall_comments")
