# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, SizeViewSet, ColorViewSet,
    AttributeViewSet, AttributeValueViewSet, ProductImageViewSet, ProductVariantViewSet
)

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')
router.register('sizes', SizeViewSet, basename='size')
router.register('colors', ColorViewSet, basename='color')
router.register('attributes', AttributeViewSet, basename='attribute')
router.register('attribute-values', AttributeValueViewSet, basename='attribute-value')
router.register('images', ProductImageViewSet, basename='product-image')
router.register('variants', ProductVariantViewSet, basename='product-variant')

urlpatterns = [
    path('', include(router.urls)),
]
