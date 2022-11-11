from django.contrib import admin
from .models import Follower


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ("__str__",  "id")
    search_fields = ("__str__", "id")

