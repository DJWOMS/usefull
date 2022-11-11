from django.contrib import admin
from django.utils.safestring import mark_safe

from src.support.models import Ticket, Category, Guide, Faq


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'status', 'create_date']
    list_filter = ['status']
    search_fields = ['title', 'user']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="500" height="400"')

    get_image.short_description = "Изображение"


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ('title',)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'most']
    list_display_links = ('question',)
    list_filter = ('most',)


admin.site.register(Category)
