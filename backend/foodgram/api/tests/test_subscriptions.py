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

    def test_user_subscriptions_list(self):
        """Авторизованные пользователи. Мои подписки.
        Возвращает пользователей, на которых подписан текущий пользователь. В
        выдачу добавляются рецепты."""

    def test_user_subscriptions_add_item(self):
        """Авторизованные пользователи. Подписаться на пользователя.
        Доступно только авторизованным пользователям."""

    def test_user_subscriptions_delete_item(self):
        """Авторизованные пользователи. Отписаться от пользователя.
        Доступно только авторизованным пользователям."""
