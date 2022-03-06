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

    def test_user_download_shopping_cart(self):
        """Авторизованные пользователи. Скачать список покупок.
        Скачать файл со списком покупок. Это может быть TXT/PDF/CSV. Важно,
        чтобы контент файла удовлетворял требованиям задания. Доступно только
        авторизованным пользователям."""

    def test_user_shopping_cart_add_item(self):
        """Авторизованные пользователи. Добавить рецепт в список покупок.
        Доступно только авторизованным пользователям."""

    def test_user_shopping_cart_delete_item(self):
        """Авторизованные пользователи. Удалить рецепт из списка покупок.
        Доступно только авторизованным пользователям."""
