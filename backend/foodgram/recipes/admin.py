from django.contrib import admin

from .forms import TagModelForm
from .models import Tag, MeasurementUnit, Ingredient, Recipe


@admin.register(Tag)
class TagModel(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'color']
    readonly_fields = ('id',)
    form = TagModelForm


admin.site.register(MeasurementUnit)
admin.site.register(Ingredient)
admin.site.register(Recipe)
