from rest_framework import generics, permissions, views, response
from rest_framework.response import Response

from src.profiles.models import Profile
from .models import Follower
from .serializers import FollowerListSerializer, FollowingListSerializer
from ..base.classes import StandardResultsSetPagination


class FollowerListView(views.APIView):
    """ Вывод списка подписчиков пользователя """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        followers = Follower.objects.filter(user__id=self.request.user.id)
        following = Follower.objects.filter(subscriber__id=self.request.user.id)
        ser_followers = FollowerListSerializer(followers, many=True)
        ser_following = FollowingListSerializer(following, many=True)
        # username = self.request.query_params.get('username')
        # if username:
        #     followers = Follower.objects.filter(
        #         user__id=self.request.user.id,
        #         subscriber__username__icontains=username
        #     )
        # return Response([ser_followers.data, ser_following.data])
        return Response({
            'followers': [dict(k.get('subscriber')) for k in ser_followers.data],
            'following': [dict(k.get('user')) for k in ser_following.data]
        })


# class FollowingListView(generics.ListAPIView):
#     """ Вывод списка на кого подписан пользователь """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = FollowingListSerializer
#     pagination_class = StandardResultsSetPagination
#
#     def get_queryset(self):
#         following = Follower.objects.filter(subscriber__id=self.request.user.id)
#         username = self.request.query_params.get('username')
#         if username:
#             following = Follower.objects.filter(
#                 subscriber__id=self.request.user.id,
#                 user__username__icontains=username
#             )
#         return following


class FollowerView(views.APIView):
    """ Добавление в подписчики """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            following = Profile.objects.get(id=pk)
        except:
            return response.Response(status=404)
        if following == request.user:
            return response.Response(status=400)
        Follower.objects.get_or_create(subscriber=request.user, user=following)
        return response.Response(status=201)

    def delete(self, request, pk):
        try:
            sub = Follower.objects.get(subscriber=self.request.user, user__id=pk)
        except:
            return response.Response(status=404)
        sub.delete()
        return response.Response(status=204)


class FollowingView(views.APIView):
    """ Удаление подписчика """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            sub = Follower.objects.get(subscriber__id=pk, user=self.request.user)
        except:
            return response.Response(status=404)
        sub.delete()
        return response.Response(status=204)
