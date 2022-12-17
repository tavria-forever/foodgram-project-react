from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import FavouriteRecipe, Ingredient, Recipe, Tag
from users.models import Follow, User

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavouriteSerializer, FollowCreateDeleteSerializer,
                          FollowListSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.select_related('measurement_unit').all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            self.permission_classes = (IsOwnerOrReadOnly,)
        elif self.action in ['create']:
            self.permission_classes = (IsAuthenticated,)
        return super(self.__class__, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @action(
    #     methods=['get', 'patch'],
    #     detail=False,
    #     url_path='me',
    #     permission_classes=(IsAuthenticated,),
    # )


class FollowListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer


class FollowCreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowCreateDeleteSerializer

    def create(self, request, *args, **kwargs):
        try:
            current_user_id = self.request.user.id
            author = get_object_or_404(User, pk=kwargs.get('author_id'))
            if author.id == current_user_id:
                raise ValidationError(
                    detail='Нельзя подписываться на самого себя'
                )
            data = {'user': current_user_id, 'author': author.id}
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
        except Http404:
            return Response(
                {'errors': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except IntegrityError:
            return Response(
                {'errors': 'Пользователь уже подписан'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response(
                {'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(
                Follow, user=self.request.user, author=kwargs.get('author_id')
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {'errors': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )


class FavouriteCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = FavouriteRecipe.objects.all()
    serializer_class = FavouriteSerializer
