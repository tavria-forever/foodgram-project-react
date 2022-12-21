from django.contrib import admin

from .models import ShoppingOrder


@admin.register(ShoppingOrder)
class ShoppingOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
