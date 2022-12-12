from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='tag_name_slug_unique',
            ),
        ]
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return (
            f'{self.name[:15]} {self.slug[:15]}, {self.color}'
        )


class MeasurementUnit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        null=True,
        to_field='name',
        on_delete=models.SET_NULL,
        related_name='ingredients'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredient_name_measurement_unit_unique',
            ),
        ]
        ordering = ('name', 'measurement_unit',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return (
            f'{self.name[:15]} / {self.measurement_unit}'
        )


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to="recipes/",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return (
            f'{self.name[:15]}'
        )


class RecipeTag(models.Model):
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )
    tag_id = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )

    def __str__(self):
        return (
            f'RecipeTag(id={self.id}, recipe_id={self.recipe_id}, tag_id'
            f'={self.tag_id})'
        )


class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return (
            f'RecipeIngredient(id={self.id}, recipe_id={self.recipe_id}, ingredient_id'
            f'={self.ingredient_id}, amount={self.amount})'
        )


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favourite_user_recipe_unique',
            ),
        ]

    def __str__(self):
        return (
            f'FavouriteRecipe(id={self.id}, user={self.user}, recipe'
            f'={self.recipe})'
        )
