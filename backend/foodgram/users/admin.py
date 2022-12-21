from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'username',
        'email',
    )
    search_fields = (
        'first_name',
        'last_name',
        'username',
    )


admin.site.register(Follow)
