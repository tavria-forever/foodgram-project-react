from django.contrib import admin

from .models import Tag, MeasurementUnit, Ingredient, Recipe

admin.site.register(Tag)
admin.site.register(MeasurementUnit)
admin.site.register(Ingredient)
admin.site.register(Recipe)
