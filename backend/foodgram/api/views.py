from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from receipts.models import Tag
from .serializers import TagSerializer


class ListRetrieveViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    permission_classes = (AllowAny, )
    lookup_field = 'id'


class TagViewSet(ListRetrieveViewSet):
    search_fields = ('slug',)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
