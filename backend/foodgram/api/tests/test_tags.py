from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import include, path
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

from recipes.models import Ingredient, IngredientRecipeRelation, Recipe, Tag

User = get_user_model()


class APITests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    fixtures = ('users.json', 'recipes.json',)

    user: User
    tag: Tag

    user_client: APIClient
    anon_client: APIClient

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_object_or_404(User, pk=2)
        cls.tag = get_object_or_404(Tag, pk=1)

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

    def __tag_list(self, apiclient):
        endpoint = reverse('api:tags-list')

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.tag.pk)
        self.assertEqual(response.data[0]['slug'], self.tag.slug)
        self.assertEqual(len(response.data), Tag.objects.all().count())

    def __tag_detail(self, apiclient):
        endpoint = reverse('api:tags-detail', args=(self.tag.pk,))

        response = apiclient.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.tag.pk)
        self.assertEqual(response.data['slug'], self.tag.slug)

    def test_anon_tag_list(self):
        """Неавторизованные пользователи. Список тегов."""

        self.__tag_list(self.anon_client)

    def test_anon_tag_detail(self):
        """Неавторизованные пользователи. Получение тега."""

        self.__tag_detail(self.anon_client)

    def test_user_tag_list(self):
        """Авторизованные пользователи. Список тегов."""

        self.__tag_list(self.user_client)

    def test_user_tag_detail(self):
        """Авторизованные пользователи. Получение тега."""

        self.__tag_detail(self.user_client)
