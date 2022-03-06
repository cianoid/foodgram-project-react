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

    def test_anon_endpoint_access(self):
        """Неавторизованные пользователи. Доступ к ресурсам API."""

    def test_user_endpoint_access(self):
        """Авторизованные пользователи. Доступ к ресурсам API."""
