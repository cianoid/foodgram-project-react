from rest_framework import serializers

from receipts.models import Ingridient, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngirdientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingridient
