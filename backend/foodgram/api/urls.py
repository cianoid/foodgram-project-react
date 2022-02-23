from django.urls import include, path
from rest_framework import routers

from .views import IngridientViewSet, TagViewSet


router = routers.DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingridients', IngridientViewSet, basename='ingridients')

urlpatterns = [
    path('', include(router.urls)),
]
