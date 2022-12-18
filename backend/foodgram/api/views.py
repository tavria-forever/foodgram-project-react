from django.db import IntegrityError
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import FavouriteRecipe, Ingredient, Recipe, Tag
from shopping_cart.models import ShoppingOrder
from users.models import Follow, User

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    FavouriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


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
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        query_params = self.request.query_params
        is_favorited = query_params.get('is_favorited', None)
        is_in_shopping_cart = query_params.get('is_in_shopping_cart', None)
        recipe_query = Recipe.objects.select_related('author')
        if is_favorited is not None:
            return recipe_query.filter(favourites__user=user)
        elif is_in_shopping_cart is not None:
            return recipe_query.filter(shopping_orders__user=user)
        return recipe_query.all()

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            self.permission_classes = (IsOwnerOrReadOnly,)
        elif self.action in ['create']:
            self.permission_classes = (IsAuthenticated,)
        return super(self.__class__, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def create_destroy_favorite(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                data = {
                    'user': self.request.user.id,
                    'recipe': kwargs.get('pk'),
                }
                serializer = FavouriteSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST
                )
            except IntegrityError:
                return Response(
                    {'errors': 'Пользователь уже подписан на этот рецепт'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == 'DELETE':
            try:
                instance = get_object_or_404(
                    FavouriteRecipe,
                    user=self.request.user,
                    recipe=kwargs.get('pk'),
                )
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Http404:
                return Response(
                    {'errors': 'Избранный рецепт не найден'},
                    status=status.HTTP_404_NOT_FOUND,
                )

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        user = request.user
        try:
            shopping_recipes = Recipe.objects.filter(
                shopping_orders__user=user
            )
            ingredients = shopping_recipes.values_list(
                'recipeingredient__ingredient__name',
                'recipeingredient__ingredient__measurement_unit',
            ).order_by('recipeingredient__ingredient__name')
            total = ingredients.annotate(
                amount=Sum('recipeingredient__amount')
            )
            shopping_cart = 'Список ингредиентов для покупки:'
            for index, ingredient in enumerate(total):
                shopping_cart += (
                    f'\n- {ingredient[0]}: {ingredient[2]} {ingredient[1]}'
                )
            return HttpResponse(shopping_cart, content_type='text/plain')
        except:
            raise Exception('Список покупок пуст')

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def create_destroy_shopping_order(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                data = {
                    'user': self.request.user.id,
                    'recipe': kwargs.get('pk'),
                }
                serializer = ShoppingCartSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST
                )
            except IntegrityError:
                return Response(
                    {
                        'errors': 'Пользователь уже добавил в корзину этот рецепт'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == 'DELETE':
            try:
                instance = get_object_or_404(
                    ShoppingOrder,
                    user=self.request.user,
                    recipe=kwargs.get('pk'),
                )
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Http404:
                return Response(
                    {'errors': 'Избранный рецепт не найден'},
                    status=status.HTTP_404_NOT_FOUND,
                )


class FollowListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)


class FollowCreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

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
