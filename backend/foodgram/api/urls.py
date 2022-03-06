from django.urls import include, path
from rest_framework import routers

from api.views import (download_shopping_cart, IngredientViewSet,
                       FavoriteManageView, ListFollowViewSet, RecipeViewSet,
                       ShoppingCartManageView, SubscriptionsManageView,
                       TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

subscriptions_urlpatterns = [
    path('subscriptions/', ListFollowViewSet.as_view()),
    path('<int:pk>/subscribe/', SubscriptionsManageView.as_view()),
]
recipe_additional_urlpatterns = [
    path(
        'download_shopping_cart/', download_shopping_cart,
        name='download_shopping_cart'),
    path('<int:pk>/shopping_cart/', ShoppingCartManageView.as_view()),
    path('<int:pk>/favorite/', FavoriteManageView.as_view()),
]

urlpatterns = [
    path('recipes/', include(recipe_additional_urlpatterns)),
    path('users/', include(subscriptions_urlpatterns)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
