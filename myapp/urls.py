from django.urls import path
from myapp import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product-images/', views.ImagesListView.as_view(), name='product-image-list'),
    path('product-images/<int:pk>/', views.ImageDetailView.as_view(), name='product-image-detail'),
    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
