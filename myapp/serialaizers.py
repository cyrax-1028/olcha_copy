from rest_framework import serializers
from .models import Category, Product, ProductImage, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    # discounted_price = serializers.ReadOnlyField()
    # get_rating = serializers.ReadOnlyField()
    # is_liked = serializers.SerializerMethodField()
    #
    # def get_is_liked(self, obj):
    #     user = self.context.get("request").user
    #     if not user.is_authenticated:
    #         return False
    #
    #     if user not in obj.like.all():
    #         return False
    #
    #     return True


    class Meta:
        model = Product
        exclude = ("created_at", "updated_at", "description", "like")


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.title', read_only=True)
    discounted_price = serializers.ReadOnlyField()
    get_rating = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        if not user.is_authenticated:
            return False

        if user not in obj.like.all():
            return False

        return True

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at", "description", "like")


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

