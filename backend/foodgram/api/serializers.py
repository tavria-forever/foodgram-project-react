from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseDjoserUserCreateSerializer

from users.models import User
from recipes.models import Tag, Ingredient, Recipe
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


class RecipeSerializer(serializers.ModelSerializer):
    image = RecipeImageField(max_length=None, use_url=True)
    # author = UserSerializer()
    # tags = TagSerializer(many=True)
    # ingredients = IngredientSerializer(many=True)

    author = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True
    )
    tags = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        many=True,
    )
    ingredients = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        many=True,
    )

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    # def create(self, validated_data):
    #     print(f'validated_data {validated_data}')
    #
    #     return Recipe(**validated_data)

    def get_is_favorited(self, obj):
        return True

    def get_is_in_shopping_cart(self, obj):
        return True

    class Meta:
        model = Recipe
        fields = '__all__'
