from rest_framework import serializers
from .models import Course, Category, Students, Lesson, Author, Task, Comment, RealizationTask
from ..base.serializers import ModelSerializer
from ..profiles.serializers import ProfileSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    """ Category list serializer """
    class Meta:
        model = Category
        fields = ("id", "name")


class AuthorSerializer(ModelSerializer):
    """ Author list serializer """
    user = ProfileSerializer()

    class Meta:
        model = Author
        fields = ("user",)


class CourseListSerializer(serializers.ModelSerializer):
    """ Course list serializer """
    authors = AuthorSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ("id", "name", "image", "authors", "lesson_count", "student_count")


class CourseSerializer(serializers.ModelSerializer):
    """ Course detail """
    category = serializers.ReadOnlyField(source='category.name')
    authors = AuthorSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ("id", "category", "name", "image", "description", "authors", "lesson_count",
                  "student_count")


class StudentSerializer(serializers.ModelSerializer):
    """ Student detail serializer """
    class Meta:
        model = Students
        fields = ("course",)


class LessonListSerializer(serializers.ModelSerializer):
    """ Lesson list serializer"""
    class Meta:
        model = Lesson
        fields = ("id", "name", "image")


class LessonSerializer(serializers.ModelSerializer):
    """ Lesson detail serializer"""
    class Meta:
        model = Lesson
        fields = ("id", "name", "text")


class RealizationTaskSerializer(serializers.ModelSerializer):
    """ RealizationTask detail serializer """
    class Meta:
        model = RealizationTask
        fields = ("task", "answer", "comment")


class RealizationTaskListSerializer(serializers.ModelSerializer):
    """ RealizationTask list serializer """
    class Meta:
        model = RealizationTask
        fields = ("answer", "success")


class TaskListSerializer(serializers.ModelSerializer):
    """ Task list serializer """
    realization_tasks = RealizationTaskListSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ("id", "title", "text", "realization_tasks")


class CommentSerializer(serializers.ModelSerializer):
    """ Comment detail serializer"""
    class Meta:
        model = Comment
        fields = ("id", "lesson", "text", "parent")


class CommentChildrenListSerializer(ModelSerializer):
    """ Comment children list serializer"""
    user = ProfileSerializer()

    class Meta:
        model = Comment
        fields = ("id", "user", "text")


class CommentListSerializer(ModelSerializer):
    """ Comment list serializer """
    user = ProfileSerializer()
    children = CommentChildrenListSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ("id", "user", "text", "children")
