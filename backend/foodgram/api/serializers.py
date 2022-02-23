from rest_framework import serializers

from receipts.models import Ingredient, Receipt, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Receipt
