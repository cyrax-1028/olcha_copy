from rest_framework import serializers
from myapp.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"