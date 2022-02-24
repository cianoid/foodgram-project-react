from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerializer)
from recipes.models import Ingredient, Recipe, Tag


class ListRetrieveViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    # @TODO Check it
    permission_classes = (AllowAny, )
    lookup_field = 'id'


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    search_fields = ('slug',)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    lookup_field = 'id'
    # @TODO Check it
    permission_classes = (AllowAny, )
