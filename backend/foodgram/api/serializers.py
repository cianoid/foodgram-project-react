from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed')
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializerList(serializers.ModelSerializer):
    author = AuthorSerializer(required=False, many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Recipe
