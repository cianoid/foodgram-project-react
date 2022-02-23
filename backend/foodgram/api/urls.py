from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, ReceiptViewSet, TagViewSet


router = routers.DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('receipts', ReceiptViewSet, basename='receipts')

urlpatterns = [
    path('', include(router.urls)),
]
