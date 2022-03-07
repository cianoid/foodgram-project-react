from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import include, path
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

from recipes.models import (Ingredient, IngredientRecipeRelation, Favorite,
                            Recipe, Tag)

User = get_user_model()


class APITests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    fixtures = ('users.json', 'recipes.json',)

    user: User
    recipe: Recipe

    user_client: APIClient
    anon_client: APIClient

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_object_or_404(User, pk=2)
        cls.recipe = get_object_or_404(Recipe, pk=1)

    @classmethod
    def tearDownClass(cls):
        IngredientRecipeRelation.objects.all().delete()
        Tag.objects.all().delete()
        Ingredient.objects.all().delete()
        Recipe.objects.all().delete()
        User.objects.all().delete()

    def setUp(self):
        self.anon_client = APIClient()

        self.user_client = APIClient()
        self.user_client.force_authenticate(user=self.user)

    def tearDown(self):
        Favorite.objects.all().delete()

    def test_user_favorites_add_item(self):
        """Авторизованные пользователи. Добавить рецепт в избранное."""

        endpoint = reverse('api:favorites', args=(self.recipe.pk,))
        recipes_in_cart_count_0 = Favorite.objects.all().count()

        response = self.user_client.post(endpoint)
        recipes_in_cart_count_1 = Favorite.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(recipes_in_cart_count_1, recipes_in_cart_count_0 + 1)
        self.assertEqual(self.user.favorites.get().recipe, self.recipe)

        response = self.user_client.post(endpoint)
        recipes_in_cart_count_2 = Favorite.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(recipes_in_cart_count_2, recipes_in_cart_count_1)

    def test_user_favorites_delete_item(self):
        """Авторизованные пользователи. Удалить рецепт из избранного."""

        endpoint = reverse('api:favorites', args=(self.recipe.pk,))
        Favorite.objects.create(user=self.user, recipe=self.recipe)
        recipes_in_cart_count_0 = Favorite.objects.all().count()
        self.assertEqual(recipes_in_cart_count_0, 1)

        response = self.user_client.delete(endpoint)
        recipes_in_cart_count_1 = Favorite.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(recipes_in_cart_count_1, recipes_in_cart_count_0 - 1)

        response = self.user_client.delete(endpoint)
        recipes_in_cart_count_2 = Favorite.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(recipes_in_cart_count_2, recipes_in_cart_count_1)
