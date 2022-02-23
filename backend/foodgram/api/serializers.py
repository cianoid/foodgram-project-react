from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Recipe
