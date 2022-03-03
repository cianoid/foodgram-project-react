import base64
import mimetypes

import djoser.serializers
from django.contrib.auth import get_user_model
from rest_framework.settings import api_settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (Ingredient, IngredientRecipeRelation, Recipe,
                            ShoppingCart, Subscription, Tag)

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
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientRecipeRelationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit')

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = IngredientRecipeRelation


class RecipeSerializerList(serializers.ModelSerializer):
    author = AuthorSerializer(required=False, many=False, read_only=True)
    tags = TagSerializer(required=False, many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        return IngredientRecipeRelationSerializer(
            IngredientRecipeRelation.objects.filter(recipe=obj).all(),
            many=True).data

    class Meta:
        exclude = ('created', )
        model = Recipe


class IngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(required=True)

    class Meta:
        fields = ('id', 'amount')
        model = IngredientRecipeRelation


class ImageBase64Field(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            mime_data, image_string = data.split(';base64,')
            image_data = base64.b64decode(image_string)

            mime_type = mime_data.removeprefix('data:')
            extension = mimetypes.MimeTypes().guess_extension(mime_type)

            data = ContentFile(image_data, name=f'temp.{extension}')

        return super().to_internal_value(data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        model = User


class CustomUserCreateSerializer(djoser.serializers.UserCreateSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all())

    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')
        model = User


class RecipeShortSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'image', 'name', 'cooking_time')
        model = Recipe


class CustomUserForRecipeSerializer(serializers.ModelSerializer):
    recipes = RecipeShortSerilizer(many=True)
    # recipe_count =

    class Meta:
        fields = ('id', 'email', 'username', 'firts_name', 'last_name',
                  'is_subscribed', 'recipes')
        model = User


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientCreateSerializer(
        required=True, many=True, read_only=False)
    image = ImageBase64Field()
    author = CustomUserSerializer(required=False)

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        obj = Recipe.objects.create(**validated_data)
        obj.save()

        obj.tags.set(tags)

        for ingredient in ingredients:
            IngredientRecipeRelation.objects.create(
                recipe=obj,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            ).save()

        return obj

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields['tags'] = TagSerializer(many=True)

        representation = super().to_representation(instance)

        representation['ingredients'] = IngredientRecipeRelationSerializer(
            IngredientRecipeRelation.objects.filter(
                recipe=instance).all(), many=True).data

        return representation

    class Meta:
        exclude = ('created', )
        model = Recipe


class SubscriptionListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipes_limit = int(self.context['request'].GET.get(
            'recipes_limit', api_settings.PAGE_SIZE))

        user = get_object_or_404(User, pk=obj.pk)
        recipes = Recipe.objects.filter(author=user)[:recipes_limit]

        return RecipeShortSerilizer(recipes, many=True).data

    def get_recipes_count(self, obj):
        user = get_object_or_404(User, pk=obj.pk)

        return Recipe.objects.filter(author=user).count()

    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = User


class SubscriptionManageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all())

    class Meta:
        exclude = ('created', )
        model = Subscription
