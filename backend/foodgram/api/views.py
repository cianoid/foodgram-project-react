from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny

from api.serializers import (IngredientSerializer, RecipeSerializer,
                             RecipeSerializerList, TagSerializer)
from recipes.models import Ingredient, Recipe, Tag


class ListRetrieveViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    # @TODO Check it
    permission_classes = (AllowAny,)
    lookup_field = 'id'


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    lookup_field = 'id'
    # @TODO Check it
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializerList

        return RecipeSerializer

