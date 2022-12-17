from djoser.serializers import \
    UserCreateSerializer as BaseDjoserUserCreateSerializer
from rest_framework import serializers
import collections.abc
from recipes.models import (FavouriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from users.models import Follow, User
from shopping_cart.models import ShoppingOrder

from .fields import RecipeImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, instance):
        current_user = self.context.get('request').user
        if instance.id == current_user.id:
            return False
        if current_user.is_anonymous:
            return False
        return instance.following.filter(user=current_user).exists()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class UserCreateSerializer(BaseDjoserUserCreateSerializer):
    class Meta(BaseDjoserUserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit_id'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


def add_recipe_tags_ingredients(
    recipe_instance, tag_ids=None, ingredients_data=None
):
    if tag_ids is not None:
        tags = Tag.objects.filter(pk__in=tag_ids)
        recipe_instance.tags.set(tags)

    if ingredients_data is not None:
        for item in ingredients_data:
            ingredient_instance = Ingredient.objects.get(pk=item.get('id'))
            recipe_instance.ingredients.add(
                ingredient_instance,
                through_defaults={'amount': item.get('amount')},
            )
    return recipe_instance


class RecipeSerializer(serializers.ModelSerializer):
    image = RecipeImageField(max_length=None, use_url=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='recipeingredient_set',
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def validate(self, data):
        tags = self.initial_data.get('tags')
        if tags is None:
            raise serializers.ValidationError(detail='Cписок id тегов обязателен для заполнения')
        elif isinstance(tags, collections.abc.Sequence) is False or len(tags) == 0:
            raise serializers.ValidationError(detail='Передан невалидный список id тегов')
        ingredients = self.initial_data.get('ingredients')
        if ingredients is None:
            raise serializers.ValidationError(detail='Cписок ингредиентов обязателен для заполнения')
        elif isinstance(ingredients, collections.abc.Sequence) is False or len(ingredients) == 0:
            raise serializers.ValidationError(detail='Передан невалидный список ингредиентов')

        return data

    def create(self, validated_data):
        raw_data = self.context['request'].data
        recipe_instance = Recipe.objects.create(**validated_data)
        return add_recipe_tags_ingredients(
            recipe_instance=recipe_instance,
            tag_ids=raw_data.get('tags'),
            ingredients_data=raw_data.get('ingredients'),
        )

    def update(self, instance, validated_data):
        raw_data = self.context['request'].data
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        add_recipe_tags_ingredients(
            recipe_instance=instance,
            tag_ids=raw_data.get('tags'),
            ingredients_data=raw_data.get('ingredients'),
        )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favourites.filter(recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_orders.filter(recipe=obj.id).exists()

    class Meta:
        ordering = ('-id',)
        model = Recipe
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        recipe_instances = instance.author.recipes.filter(
            author=instance.author.id,
        ).order_by('-id')
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit', None
        )
        if recipes_limit is not None:
            recipe_instances = recipe_instances[:int(recipes_limit)]
        recipes = []
        for recipe in recipe_instances.values('id', 'name', 'image', 'cooking_time'):
            recipes.append(
                {
                    'id': recipe.get('id'),
                    'name': recipe.get('name'),
                    'image': recipe.get('image'),
                    'cooking_time': recipe.get('cooking_time'),
                }
            )
        
        return {
            'id': instance.author.id,
            'email': instance.author.email,
            'username': instance.author.username,
            'first_name': instance.author.first_name,
            'last_name': instance.author.last_name,
            'recipes_count': instance.author.recipes.count(),
            'is_subscribed': True,
            'recipes': recipes,
        }

    class Meta:
        model = Follow
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.recipe.id,
            'name': instance.recipe.name,
            'image': str(instance.recipe.image),
            'cooking_time': instance.recipe.cooking_time,
        }
    
    class Meta:
        model = FavouriteRecipe
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.recipe.id,
            'name': instance.recipe.name,
            'image': str(instance.recipe.image),
            'cooking_time': instance.recipe.cooking_time,
        }

    class Meta:
        model = ShoppingOrder
        fields = '__all__'
