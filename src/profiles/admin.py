from django.contrib import admin
from .models import Profile, Technology, Account, AccountEmail


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'id']
    search_fields = ['username']

    class Meta:
        model = Profile


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name', 'id']

    class Meta:
        model = Technology


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['profile', 'provider', 'id']
    search_fields = ['provider']
    readonly_fields = ('account_id', 'provider')


@admin.register(AccountEmail)
class AccountEmailAdmin(admin.ModelAdmin):
    list_display = ['profile', 'email', 'id']
    search_fields = ['email']
    fieldsets = (
        ('Users', {
            'fields': (
                'profile', 'email',
            )}
         ),
    )
