from rest_framework import viewsets
from products.models import (
    Product, Category, Size, Color,
    Attribute, AttributeValue,
    ProductImage, ProductVariant
)
from products.serializers import (
    ProductSerializer, CategorySerializer,
    SizeSerializer, ColorSerializer,
    AttributeSerializer, AttributeValueSerializer,
    ProductImageSerializer, ProductVariantSerializer
)

# 🔹 Categories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

# 🔹 Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('variants', 'images', 'attributes').all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

# 🔹 Sizes
class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

# 🔹 Colors
class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

# 🔹 Attributes
class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

# 🔹 Attribute Values (optional endpoint)
class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer

# 🔹 Product Images
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

# 🔹 Product Variants
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
