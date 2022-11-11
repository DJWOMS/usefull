from django.contrib import admin
from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("get_member", "create_date", "id")

    def get_member(self, obj):
        return ",\n".join([profile.username for profile in obj.member.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "text", "create_date")
