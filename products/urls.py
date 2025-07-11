# products/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
# This file defines the URL routing for the products app, allowing access to the Product and Category viewsets.
# The DefaultRouter automatically creates the necessary routes for the viewsets.