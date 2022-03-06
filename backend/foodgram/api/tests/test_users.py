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

    def test_anon_create_account(self):
        """Неавторизованные пользователи. Создать аккаунт."""

    def test_anon_login(self):
        """Неавторизованные пользователи. Входить в систему под своим логином и
        паролем.
        Используется для авторизации по емейлу и паролю, чтобы далее
        использовать токен при запросах."""

    def test_anon_user_list(self):
        """Неавторизованные пользователи.
        Список пользователей."""

    def test_user_logout(self):
        """Авторизованные пользователи. Выходить из системы (разлогиниваться).
        Удаляет токен текущего пользователя."""

    def test_user_change_password(self):
        """Авторизованные пользователи. Менять свой пароль.
        Изменение пароля текущего пользователя."""

    def test_user_user_list(self):
        """Авторизованные пользователи. Список пользователей."""

    def test_user_user_profile(self):
        """Авторизованные пользователи. Профиль пользователя.
        Доступно всем пользователям."""

    def test_user_user_me(self):
        """Авторизованные пользователи. Текущий пользователь."""


