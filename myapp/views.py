from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from myapp.serialaizers import ProductSerializer
from myapp.models import Product


# Create your views here.

# class ProductView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request, format=None):
#         products = Product.objects.all()
#         data = []
#         for product in products:
#             data.append({
#                 'id': product.id,
#                 'name': product.name,
#                 'price': product.price,
#                 'quantity': product.quantity,
#             })
#
#         return Response(data)

class ProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)

        return Response(serializers.data)