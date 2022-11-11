from rest_framework import generics, permissions, views, response

from . import serializers
from .models import Course, Category, Lesson, Task, Comment, RealizationTask, Students

from ..base.classes import CreateRetrieveUpdateDestroy
from ..base import permissions as perm


class CategoryListView(generics.ListAPIView):
    """ Category list view"""
    queryset = Category.objects.filter(is_publish=True)
    serializer_class = serializers.CategoryListSerializer


class CourseListView(generics.ListAPIView):
    """ Course list view"""
    serializer_class = serializers.CourseListSerializer

    def get_queryset(self):
        queryset = Course.objects.filter(is_publish=True)
        order = self.request.query_params.get('order')
        category = self.request.query_params.get('category')

        if category:
            queryset = queryset.filter(category=category)
        if order:
            queryset = queryset.order_by('name')
        return queryset


class CourseView(generics.RetrieveAPIView):
    """ Course detail view"""
    queryset = Course.objects.filter(is_publish=True)
    serializer_class = serializers.CourseSerializer


class SignUpForCourseView(generics.CreateAPIView):
    """ Sign up for courses view"""
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SignOutForCourseView(views.APIView):
    """ Sign out for courses view"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.StudentSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer['course'].value

            try:
                Students.objects.get(
                    user=request.user,
                    course_id=course_id
                ).delete()
            except:
                return response.Response(status=404)

            RealizationTask.objects.filter(
                user=request.user,
                task__lesson__course__id=course_id
            ).delete()

            Comment.objects.filter(
                user=request.user,
                lesson__course__id=course_id
            ).delete()

            return response.Response(status=204)

        return response.Response(serializer.errors, status=400)


class LessonListView(generics.ListAPIView):
    """ Lesson list view """
    serializer_class = serializers.LessonListSerializer
    permission_classes = [permissions.IsAuthenticated, perm.IsSignUpForCourseAndLesson]

    def get_queryset(self):
        return Lesson.objects.filter(course=self.kwargs['pk'], is_publish=True)


class LessonView(generics.RetrieveAPIView):
    """ Lesson detail view"""
    queryset = Lesson.objects.filter(is_publish=True)
    serializer_class = serializers.LessonSerializer
    permission_classes = [permissions.IsAuthenticated, perm.IsSignUpForLessonAndTask]


class TaskListView(generics.ListAPIView):
    """ Lesson list view"""
    serializer_class = serializers.TaskListSerializer
    permission_classes = [permissions.IsAuthenticated, perm.IsSignUpForLessonAndTask]

    def get_queryset(self):
        return Task.objects.filter(lesson=self.kwargs['pk'], is_publish=True)


class RealizationTaskView(CreateRetrieveUpdateDestroy):
    """ CRUD RealizationTask view"""
    queryset = RealizationTask.objects.all()
    serializer_class = serializers.RealizationTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {'retrieve': [perm.IsAuthor],
                                    'create': [perm.IsSignUpForRealizationTask],
                                    'update': [perm.IsAuthor],
                                    'destroy': [perm.IsAuthor]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(CreateRetrieveUpdateDestroy):
    """ CRUD Comment view"""
    queryset = Comment.objects.filter(is_delete=False)
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes_by_action = {'create': [perm.IsSignUpForComment],
                                    'update': [perm.IsAuthor],
                                    'destroy': [perm.IsAuthor]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

    def perform_update(self, instance):
        instance.save(user=self.request.user)


class CommentListView(generics.ListAPIView):
    """ Comment list view"""
    serializer_class = serializers.CommentListSerializer
    permission_classes = [permissions.IsAuthenticated, perm.IsSignUpForLessonAndTask]

    def get_queryset(self):
        return Comment.objects.filter(lesson=self.kwargs['pk'], is_delete=False, parent=None)
