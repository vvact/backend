
# products/urls.py
from django.urls import path, include
# Importing the router from the products app

from rest_framework.routers import DefaultRouter
from products.views import (
    CategoryViewSet, ProductViewSet, SizeViewSet, ColorViewSet,
    AttributeViewSet, AttributeValueViewSet,
    ProductImageViewSet, ProductVariantViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'attribute-values', AttributeValueViewSet)
router.register(r'images', ProductImageViewSet)
router.register(r'variants', ProductVariantViewSet)

urlpatterns = router.urls
