from django_filters import rest_framework as django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        field_name='tags', lookup_expr='slug')
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        recipes = queryset.filter(pk__in=[
            cart_item.recipe.pk
            for cart_item
            in self.request.user.shopping_cart.all()])

        return recipes

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
