from django.contrib.auth import authenticate
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Group, Product, ProductImage, Comment, ProductAttribute, Order
from .serialaizers import (
    CategorySerializer, GroupSerializer, ProductSerializer, ProductDetailSerializer,
    ProductImageSerializer, CommentSerializer, CategoryDetailSerializer,
    ProductCreateSerializer, OrderSerializer, GroupDetailSerializer, OrderDetailSerializer, RegisterSerializer
)
from myapp.permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related("category").all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GroupDetailSerializer
        return GroupSerializer

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "group").prefetch_related(
        Prefetch("images", queryset=ProductImage.objects.all()),
        Prefetch("product_attributes", queryset=ProductAttribute.objects.all())
    )
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ProductCreateSerializer
        return ProductSerializer

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CommentListView(ListCreateAPIView):
    queryset = Comment.objects.select_related("product", "user").all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CommentByProductView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return Comment.objects.filter(product_id=product_id).select_related("user")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return OrderDetailSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        product = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        product_obj = Product.objects.filter(id=product).first()
        if product_obj and product_obj.quantity < quantity:
            return Response({"error": "Yetarli mahsulot mavjud emas!"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ///////////////////////// J W T ////////////////////////////////

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Foydalanuvchi muvaffaqiyatli yaratildi!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"error": "Noto‘g‘ri username yoki parol"}, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Tizimdan chiqildi"}, status=200)
        except Exception as e:
            return Response({"error": "Noto‘g‘ri token"}, status=400)
