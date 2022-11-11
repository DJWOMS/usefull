from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, generics, parsers, viewsets

from .models import Profile, Technology, ColorSchema
from . import serializers

from .services.service import progress_service, validate_size_image, delete_old_file
from ..base.classes import StandardResultsSetPagination


class TechnologyListView(generics.ListAPIView):
    """ Technology list view """
    queryset = Technology.objects.all()
    serializer_class = serializers.TechnologyListSerializer
    permission_classes = [permissions.IsAuthenticated]


class TechnologyDeleteView(APIView):
    """ Technology delete view """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        technology = get_object_or_404(Technology, id=id)
        try:
            request.user.technology.remove(technology)
        except:
            return Response(status=400)
        return Response(status=204)


class ProfileListView(generics.ListAPIView):
    """ Profile list and search """
    serializer_class = serializers.GetProfilePublicSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        profiles = Profile.objects.all().order_by('username')

        username = self.request.query_params.get('username')
        # email = self.request.query_params.get('email')

        if username:
            profiles = Profile.objects.filter(username__icontains=username)
        # if email:
        #     profiles = Profile.objects.filter(email__icontains=email)

        return profiles


class ProfilePublicView(ModelViewSet):
    """ Вывод публичного профиля пользователя """
    queryset = Profile.objects.all()
    serializer_class = serializers.GetProfilePublicSerializer
    permission_classes = [permissions.AllowAny]


class ProfilePrivateView(generics.RetrieveUpdateAPIView):
    """ Вывод профиля пользователя """
    serializer_class = serializers.GetProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj
    

class ProfileAvatarView(viewsets.ModelViewSet):
    """ Изменение аватара пользователя """
    serializer_class = serializers.GetProfileAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.MultiPartParser,)

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        delete_old_file(instance.avatar.path)
        instance.avatar = None
        instance.save()


class ProgressView(APIView):
    """ Student progress view """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: serializers.ProgressSerializer()})
    def get(self, request):
        serializer = serializers.ProgressSerializer(data={
            "course_signup_count": progress_service.course_signup_count(request.user),
            "lesson_success": progress_service.lesson_success_count(request.user),
            "lesson_non_success": progress_service.lesson_non_success_count(request.user),
            "task_count": progress_service.task_count(request.user),
            "task_success_count": progress_service.task_success_count(request.user)
        })
        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors)


class ColorSchemaView(viewsets.ModelViewSet):
    """ Color scheme of user
    """
    serializer_class = serializers.ColorSchemaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = ColorSchema.objects.get_or_create(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
