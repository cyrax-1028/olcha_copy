from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp import views
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register("categories", views.CategoryViewSet, basename="category")
router.register("groups", views.GroupViewSet, basename="group")
router.register("products", views.ProductViewSet, basename="product")
router.register(r"orders", views.OrderViewSet, basename="order")

urlpatterns = [
    path("comments/", views.CommentListView.as_view()),
    path("comment-by-product/<int:product_id>", views.CommentByProductView.as_view()),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += [
    path("", include(router.urls)),
]
