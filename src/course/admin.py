from django.contrib import admin
from django import forms

from .models import Category, Course, Lesson, Task, RealizationTask, Students, Comment, Author

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Course
        fields = '__all__'


class LessonAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Lesson
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_publish']
    list_filter = ['name', 'is_publish']
    search_fields = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'authors', 'is_publish', 'id']
    list_filter = ['name', 'category', 'authors', 'is_publish']
    search_fields = ['id', 'name', 'category']
    form = CourseAdminForm

    def authors(self, obj):
        return "\n".join([str(author.user) for author in obj.authors.all()])


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    list_filter = ['user', 'course']
    search_fields = ['user', 'course']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course', 'create_date', 'is_publish']
    list_display_links = ['id', 'name']
    list_filter = ['name', 'course', 'create_date', 'is_publish']
    search_fields = ['id', 'name', 'course']
    form = LessonAdminForm


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'is_publish', 'id']
    list_filter = ['title', 'lesson', 'is_publish']
    search_fields = ['id', 'title', 'lesson']


@admin.register(RealizationTask)
class RealizationTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'user', 'success', 'create_date']
    list_display_links = ['id', 'task']
    list_filter = ['task', 'user', 'success', 'create_date']
    search_fields = ['id', 'task', 'user']


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    list_filter = ['user', 'course']
    search_fields = ['user', 'course']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'user', 'create_date', 'is_delete']
    list_filter = ['lesson', 'user', 'create_date', 'is_delete']
    search_fields = ['id', 'lesson', 'user']

