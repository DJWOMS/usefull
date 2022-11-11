from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from src.achievements.models import Achievement, Category


admin.site.register(Category)


class AchievementAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Achievement
        fields = '__all__'


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_publish', 'id']
    list_filter = ['category', 'is_publish']
    search_fields = ['id', 'name', 'category']
    form = AchievementAdminForm
