from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

User = get_user_model()


class APITests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def test_anon_recipe_list(self):
        """Неавторизованные пользователи. Список рецептов.
        Страница доступна всем пользователям. Доступна фильтрация по
        избранному, автору, списку покупок и тегам."""

    def test_anon_recipe_detail(self):
        """Неавторизованные пользователи. Получение рецепта."""

    def test_user_recipe_list(self):
        """Авторизованные пользователи. Список рецептов.
        Страница доступна всем пользователям. Доступна фильтрация по
        избранному, автору, списку покупок и тегам."""

    def test_user_recipe_detail(self):
        """Авторизованные пользователи. Получение рецепта."""

    def test_user_recipe_create(self):
        """Авторизованные пользователи. Создание рецепта.
        Доступно только авторизованному пользователю."""

    def test_user_recipe_update(self):
        """Авторизованные пользователи. Обновление рецепта.
        Доступно только автору данного рецепта."""

    def test_user_recipe_delete(self):
        """Авторизованные пользователи. Удаление рецепта.
        Доступно только автору данного рецепта."""
