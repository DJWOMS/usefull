from rest_framework import permissions, generics, viewsets, status
from rest_framework.response import Response

from .services import post_view_count
from ..base.classes import CreateUpdateDestroy, CreateRetrieveUpdateDestroy, \
    StandardResultsSetPagination
from ..base.permissions import IsAuthor
from .models import Post, Comment
from .serializers import (PostSerializer, ListPostSerializer, CommentCreateSerializer)
from ..followers.models import Follower


class PostListView(generics.ListAPIView):
    """ Список постов на стене пользователя """
    serializer_class = ListPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        posts = Post.objects.filter(user__id=self.kwargs.get('pk'))
        follower = Follower.objects.filter(
            subscriber=self.request.user,
            user__id=self.kwargs.get('pk')
        ).first()

        if posts and self.request.user == posts.first().user:
            posts = posts
        elif follower and self.request.user == follower.subscriber:
            posts = posts.exclude(visibility='private')
        else:
            posts = posts.exclude(visibility='private')
            posts = posts.exclude(visibility='protected')

        return posts


class PostView(CreateRetrieveUpdateDestroy):
    """ CRUD поста """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().prefetch_related('wall_comments')
    serializer_class = PostSerializer
    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = post_view_count(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentsView(CreateUpdateDestroy):
    """ CRUD комментариев к запси"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes_by_action = {'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     obj = self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #
    #     return Response(obj.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        #TODO Проверить удаляет ли пользователь только свой коммент
        instance.delete()
