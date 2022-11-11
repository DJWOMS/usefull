from django.contrib import admin

from src.wall.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Посты
    """
    list_display = ("id", "user", "published", "create_date", "moderation", "view_count")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Коментарии к постам
    """
    list_display = ("user", "post", "create_date", "update_date", "is_publish", "is_delete", "id")
    # actions = ['unpublish', 'publish']

