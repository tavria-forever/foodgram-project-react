from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from recipes.models import Tag, Ingredient

from .filters import IngredientFilter
from .serializers import UserSerializer, ChangePasswordSerializer, TagSerializer, IngredientSerializer
from .permissions import UserPermissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def get_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
        permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={
            'user': request.user
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
