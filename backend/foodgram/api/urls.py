from django.urls import include, path
from rest_framework import routers

from .views import (
    FollowCreateDestroyViewSet,
    FollowListViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(
    r'users/(?P<author_id>\d+)/subscribe',
    FollowCreateDestroyViewSet,
    basename='subscribe',
)
router.register(
    r'users/subscriptions', FollowListViewSet, basename='subscriptions'
)
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
