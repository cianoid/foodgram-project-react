from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from receipts.models import Ingridient, Tag
from .serializers import IngirdientSerializer, TagSerializer


class ListRetrieveViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    permission_classes = (AllowAny, )
    lookup_field = 'id'


class TagViewSet(ListRetrieveViewSet):
    search_fields = ('slug',)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(ListRetrieveViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngirdientSerializer
