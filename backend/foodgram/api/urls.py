from django.urls import include, path
from rest_framework import routers

from api.views import (IngredientViewSet, ListFollowViewSet, RecipeViewSet,
                       SubscriptionsManageView, TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

subscriptions_urlpatterns = [
    path('subscriptions/', ListFollowViewSet.as_view()),
    path('<int:pk>/subscribe/', SubscriptionsManageView.as_view()),
]

urlpatterns = [
    path('users/', include(subscriptions_urlpatterns)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
