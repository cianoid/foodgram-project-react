import csv

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, viewsets, permissions,
                            status)
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view, permission_classes

from api.filters import RecipeFilter
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             RecipeSerializerList, RecipeShortSerilizer,
                             SubscriptionListSerializer, TagSerializer)
from recipes.models import (Ingredient, IngredientRecipeRelation, Recipe,
                            ShoppingCart, Subscription, Tag)

User = get_user_model()


class ListRetrieveViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    # @TODO Check it
    permission_classes = (permissions.AllowAny,)


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

    # @TODO Check it
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializerList

        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscriptionsManageView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        author = get_object_or_404(User, pk=pk)
        user = request.user

        if author == user:
            return Response(
                {'errors': 'Вы не можете подписываться на себя'},
                status=status.HTTP_400_BAD_REQUEST)

        if Subscription.objects.filter(author=author, user=user).exists():
            return Response(
                {'errors': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST)

        obj = Subscription(author=author, user=user)
        obj.save()

        serializer = SubscriptionListSerializer(
            author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        user = request.user
        author = get_object_or_404(User, id=pk)

        try:
            Subscription.objects.get(author=author, user=user).delete()
        except Subscription.DoesNotExist:
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFollowViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(subscripters__user=user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_shopping_cart(request):
    recipes = request.user.shopping_cart.all().values('recipe_id')
    ingredients = IngredientRecipeRelation.objects.filter(recipe__in=recipes)

    if not ingredients:
        return Response(
            {'errors': 'Ваш список для покупок пустой'},
            status=status.HTTP_204_NO_CONTENT)

    total_ingredients = {}

    # @TODO изучить функции агрегирования
    for ingredient in ingredients:
        ing = ingredient.ingredient

        try:
            total_ingredients[ing.pk][1] += ingredient.amount
        except KeyError:
            total_ingredients[ing.pk] = [
                ing.name,
                ingredient.amount,
                ing.measurement_unit]

    response = HttpResponse(content_type='text/csv', status=status.HTTP_200_OK)
    response['Content-Disposition'] = 'attachment; filename="shoppingcart.csv"'

    writer = csv.writer(response)
    for ingredient in total_ingredients.values():
        writer.writerow(ingredient)

    return response


class ShoppingCartManageView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                {'errors': 'Этот рецепт уже в вашем списке покупок'},
                status=status.HTTP_400_BAD_REQUEST)

        obj = ShoppingCart(recipe=recipe, user=user)
        obj.save()

        serializer = RecipeShortSerilizer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        recipe = get_object_or_404(Recipe, id=pk)

        try:
            ShoppingCart.objects.get(recipe=recipe, user=request.user).delete()
        except ShoppingCart.DoesNotExist:
            return Response(
                {'errors': 'Этого рецепта нет в вашем списке покупок'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
