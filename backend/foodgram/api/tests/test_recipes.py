from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import include, path
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

from recipes.models import (Ingredient, IngredientRecipeRelation, Favorite, Recipe, ShoppingCart, Subscription, Tag)

User = get_user_model()


class APITests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    fixtures = ('users.json', 'recipes.json',)

    user: User
    user_follower: User
    tag: Tag
    ingredient: Ingredient
    recipe: Recipe

    recipe_count: int

    user_client: APIClient
    user_follower_client: APIClient
    anon_client: APIClient

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_object_or_404(User, pk=2)
        cls.user_follower = get_object_or_404(User, pk=3)
        cls.tag = get_object_or_404(Tag, pk=1)
        cls.ingredient = get_object_or_404(Ingredient, pk=802)
        cls.recipe = get_object_or_404(Recipe, pk=1)

        cls.recipe_count = Recipe.objects.all().count()

        for model in [Favorite, ShoppingCart]:
            model.objects.create(user=cls.user_follower, recipe=cls.recipe)

    @classmethod
    def tearDownClass(cls):
        IngredientRecipeRelation.objects.all().delete()
        Tag.objects.all().delete()
        Ingredient.objects.all().delete()
        Recipe.objects.all().delete()
        User.objects.all().delete()
        Favorite.objects.all().delete()
        Subscription.objects.all().delete()
        ShoppingCart.objects.all().delete()

    def setUp(self):
        self.anon_client = APIClient()

        self.user_client = APIClient()
        self.user_client.force_authenticate(user=self.user)

        self.user_follower_client = APIClient()
        self.user_follower_client.force_authenticate(user=self.user_follower)

    def __recipe_list(self, apiclient):
        """Список рецептов.
        Страница доступна всем пользователям. Доступна фильтрация по
        избранному, автору, списку покупок и тегам."""

        # Запрос без параметров
        endpoint = reverse('api:recipes-list')

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.recipe_count)
        self.assertEqual(response.data['results'][0]['name'], self.recipe.name)
        self.assertIsNone(response.data['next'])

        # Пагинатор
        endpoint = reverse('api:recipes-list') + '?limit=1'

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.recipe_count)
        self.assertEqual(response.data['results'][0]['name'], self.recipe.name)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 1)

        endpoint = reverse('api:recipes-list') + '?limit=1&page=2'

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.recipe_count)
        self.assertNotEqual(
            response.data['results'][0]['name'], self.recipe.name)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 1)

        # Фильтрация по автору
        endpoint = (reverse('api:recipes-list') +
                    '?author={}'.format(self.user.pk))
        author_recipes = self.user.recipes.all()
        author_recipe_count = author_recipes.count()

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], author_recipe_count)
        self.assertEqual(
            response.data['results'][0]['name'], author_recipes[0].name)

        # Фильтрация по тегам
        endpoint = (reverse('api:recipes-list') +
                    '?tags={}'.format(self.tag.slug))
        tag1_recipe_count = self.tag.recipes.all().count()
        tag1_2_recipe_count = Tag.objects.filter(pk__in=[1, 2]).count()

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], tag1_recipe_count)

        endpoint = (reverse('api:recipes-list') +
                    '?tags={}&tags={}'.format(
                        self.tag.slug, get_object_or_404(Tag, pk=2).slug))

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], tag1_2_recipe_count)

    def __recipe_detail(self, apiclient):
        """Получение рецепта."""
        endpoint = reverse('api:recipes-detail', args=(self.recipe.pk,))

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.recipe.pk)

    def test_anon_recipe_list(self):
        """Неавторизованные пользователи. Список рецептов.
        Страница доступна всем пользователям. Доступна фильтрация по
        избранному, автору, списку покупок и тегам."""

        self.__recipe_list(self.anon_client)

        # Фильтрация по избранному
        endpoint = reverse('api:recipes-list') + '?is_favorited=1'

        response = self.anon_client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        # Фильтрация по списку покупок
        endpoint = reverse('api:recipes-list') + '?is_in_shopping_cart=1'

        response = self.anon_client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_anon_recipe_detail(self):
        """Неавторизованные пользователи. Получение рецепта."""

        self.__recipe_detail(self.anon_client)

    def test_user_recipe_list(self):
        """Авторизованные пользователи. Список рецептов.
        Страница доступна всем пользователям. Доступна фильтрация по
        избранному, автору, списку покупок и тегам."""

        self.__recipe_list(self.user_client)

        # Фильтрация по избранному
        endpoint = reverse('api:recipes-list') + '?is_favorited=1'

        response = self.user_follower_client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], 1)

        # Фильтрация по списку покупок
        endpoint = reverse('api:recipes-list') + '?is_in_shopping_cart=1'

        response = self.user_follower_client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], 1)

    def test_user_recipe_detail(self):
        """Авторизованные пользователи. Получение рецепта."""

        self.__recipe_detail(self.user_client)

