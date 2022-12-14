from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Tag, Ingredient, Recipe
from .filters import IngredientFilter, RecipeFilter
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)
from .permissions import IsOwnerOrReadOnly


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
