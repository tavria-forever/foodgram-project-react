from rest_framework import serializers

from users.models import User
from recipes.models import Tag, Ingredient


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return True

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
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Учетные данные не были предоставлены.'
            )
        return value

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['user']
        user.set_password(password)
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
