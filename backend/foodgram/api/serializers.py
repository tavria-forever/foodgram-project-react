from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseDjoserUserCreateSerializer

from users.models import User
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from .fields import RecipeImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return True
        # user = self.context.get('request').user
        # if user.is_anonymous:
        #     return False
        # return user.follower.filter(author_id=obj).exist()

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


class IngredientRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        recipe_ingredient = RecipeIngredient.objects.get(ingredient_id=obj.id)
        return recipe_ingredient.amount

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    image = RecipeImageField(max_length=None, use_url=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def create(self, validated_data):
        raw_data = self.context['request'].data
        recipe_instance = Recipe.objects.create(**validated_data)

        tags = Tag.objects.filter(pk__in=raw_data.get('tags')).all()
        recipe_instance.tags.set(tags)

        for item in raw_data.get('ingredients'):
            ingredient_instance = Ingredient.objects.get(pk=item.get('id'))
            recipe_instance.ingredients.add(
                ingredient_instance,
                through_defaults={'amount': item.get('amount')}
            )

        return recipe_instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)

        raw_data = self.context['request'].data
        tags = Tag.objects.filter(pk__in=raw_data.get('tags')).all()
        instance.tags.set(tags)

        for item in raw_data.get('ingredients'):
            ingredient_instance = Ingredient.objects.get(pk=item.get('id'))
            instance.ingredients.add(
                ingredient_instance,
                through_defaults={'amount': item.get('amount')}
            )

        instance.save()

        return instance

    def get_is_favorited(self, obj):
        return True

    def get_is_in_shopping_cart(self, obj):
        return True

    class Meta:
        model = Recipe
        fields = '__all__'
