from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from receipts.models import Ingredient, Receipt, Tag
from .serializers import IngredientSerializer, ReceiptSerializer, TagSerializer


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


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    lookup_field = 'id'
    # @TODO Check it
    permission_classes = (AllowAny, )