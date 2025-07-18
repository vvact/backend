from rest_framework import viewsets
from products.models import (
    Product, Category, Size, Color,
    Attribute, AttributeValue,
    ProductImage, ProductVariant
)
from django.db.models import Avg, Count
from products.serializers import (
    ProductSerializer, CategorySerializer,
    SizeSerializer, ColorSerializer,
    AttributeSerializer, AttributeValueSerializer,
    ProductImageSerializer, ProductVariantSerializer
)
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from random import sample
from django.db.models import Count
from django.utils import timezone

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')  # 👈 Add this
    serializer_class = CategorySerializer
    lookup_field = 'slug'

# 🔹 Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category') \
        .prefetch_related(
            'variants__size',
            'variants__color',
            'images',
            'attributes__attribute',
            'attributes__value'
        ).order_by('-created_at')  # 👈 Add ordering here
    
    queryset = Product.objects.all().annotate(
        average_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )
    serializer_class = ProductSerializer

    serializer_class = ProductSerializer
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug', 'variants__color', 'variants__size']
    search_fields = ['name', 'description']


    @action(detail=True, methods=['get'], url_path='related')
    def related_products(self, request, slug=None):
        product = self.get_object()
        related = Product.objects.filter(category=product.category).exclude(id=product.id)

        # Limit to 6 if any related are found
        if related.exists():
            related = related[:6]
        else:
            # Fallback: Return random 6 products excluding the current one
            all_others = Product.objects.exclude(id=product.id)
            count = all_others.count()
            if count <= 6:
                related = all_others
            else:
                random_ids = sample(list(all_others.values_list('id', flat=True)), 6)
                related = Product.objects.filter(id__in=random_ids)

        serializer = self.get_serializer(related, many=True)
        return Response(serializer.data)
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


