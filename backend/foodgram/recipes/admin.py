from django.contrib import admin

from .forms import TagModelForm
from .models import (
    FavouriteRecipe,
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
    search_fields = ('name',)
    readonly_fields = ('id',)
    form = TagModelForm


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    search_fields = ('name',)
    readonly_fields = ('id',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    raw_id_fields = ('ingredient',)
    extra = 0


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    raw_id_fields = ('tag',)
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'text', 'cooking_time']
    list_filter = (
        'name',
        'author',
        'tags',
    )
    list_select_related = True
    search_fields = ('name',)
    inlines = (
        RecipeIngredientInline,
        RecipeTagInline,
    )

    def change_view(self, request, object_id, form_url='', extra_content=None):
        in_favorites_count = FavouriteRecipe.objects.filter(
            recipe=object_id
        ).count()
        context = {'in_favorites_count': in_favorites_count}
        return super(RecipeAdmin, self).change_view(
            request, object_id, form_url, context
        )


admin.site.register(MeasurementUnit)
