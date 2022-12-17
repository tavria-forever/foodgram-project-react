from django.contrib import admin

from .forms import TagModelForm
from .models import (
    Ingredient,
    MeasurementUnit,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'color']
    readonly_fields = ('id',)
    form = TagModelForm


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    readonly_fields = ('id',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    raw_id_fields = ('ingredient_id',)
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    raw_id_fields = ('tag_id',)
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'text', 'cooking_time']
    inlines = (
        RecipeIngredientInline,
        RecipeTagInline,
    )


admin.site.register(MeasurementUnit)
