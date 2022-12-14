from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseDjoserUserCreateSerializer

from users.models import User, Follow
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from .fields import RecipeImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserCreateSerializer(BaseDjoserUserCreateSerializer):
    class Meta(BaseDjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password',)
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit_id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


def add_recipe_tags_ingredients(recipe_instance, tag_ids=None, ingredients_data=None):
    if tag_ids is not None:
        tags = Tag.objects.filter(pk__in=tag_ids)
        recipe_instance.tags.set(tags)

    if ingredients_data is not None:
        for item in ingredients_data:
            ingredient_instance = Ingredient.objects.get(pk=item.get('id'))
            recipe_instance.ingredients.add(
                ingredient_instance,
                through_defaults={'amount': item.get('amount')}
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

    def create(self, validated_data):
        raw_data = self.context['request'].data
        recipe_instance = Recipe.objects.create(**validated_data)
        return add_recipe_tags_ingredients(
            recipe_instance=recipe_instance,
            tag_ids=raw_data.get('tags'),
            ingredients_data=raw_data.get('ingredients')
        )

    def update(self, instance, validated_data):
        raw_data = self.context['request'].data
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        add_recipe_tags_ingredients(
            recipe_instance=instance,
            tag_ids=raw_data.get('tags'),
            ingredients_data=raw_data.get('ingredients')
        )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        return True

    def get_is_in_shopping_cart(self, obj):
        return True

    class Meta:
        ordering = ('-id',)
        model = Recipe
        fields = '__all__'


class FollowCreateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class FollowListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author_id).count()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get('recipes_limit', None)
        recipe_instances = Recipe.objects.filter(author=obj.author_id).order_by('-id')[:int(recipes_limit)]
        recipes = []
        for item in recipe_instances.values():
            recipes.append({
                'id': item.get('id'),
                'name': item.get('name'),
                'image': item.get('image'),
                'cooking_time': item.get('cooking_time')
            })
        return recipes

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count',)
