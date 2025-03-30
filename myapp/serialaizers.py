from rest_framework import serializers
from myapp.models import Category, Group, Product, ProductImage, Comment, ProductAttribute, Order
from django.urls import reverse
from django.contrib.auth.models import User


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "is_prime"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["attribute", "attribute_value"]


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_prime = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image", "is_prime", "detail_url"]

    def get_image(self, obj):
        prime_image = obj.images.filter(is_prime=True).first()
        return prime_image.image.url if prime_image else None

    def get_is_prime(self, obj):
        return obj.images.filter(is_prime=True).exists()

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(reverse('product-detail', kwargs={'pk': obj.pk}))
        return None


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.title', read_only=True)
    product_attributes = ProductAttributeSerializer(many=True, read_only=True)
    discounted_price = serializers.ReadOnlyField()
    get_rating = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        if not user.is_authenticated:
            return False
        return obj.like.filter(id=user.id).exists()

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at", "description", "like")


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "name", "group", "category", "description",
            "price", "discount", "quantity", "stock"
        ]


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'full_name', 'product', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(reverse('order-detail', kwargs={'pk': obj.pk}))
        return None


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'full_name', 'product', 'phone', 'quantity', 'status', 'total_price']


class GroupSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["id", "title","category", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(reverse('group-detail', kwargs={'pk': obj.pk}))
        return None


class GroupDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["id", "title", "products"]


class CategorySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "title", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(reverse('category-detail', kwargs={'pk': obj.pk}))
        return None


class CategoryDetailSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title", "groups"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
