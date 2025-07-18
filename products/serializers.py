from rest_framework import serializers
from products.models import (
    Product, Category, ProductImage,
    ProductVariant, Size, Color,
    Attribute, AttributeValue,
    ProductAttribute
)
from reviews.serializers import ReviewSerializer
from django.db.models import Avg


# 🔹 Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


# 🔹 Size
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']
        read_only_fields = ['id']


# 🔹 Color
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']
        read_only_fields = ['id']


# 🔹 Attribute & Value
class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']
        read_only_fields = ['id']


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values']
        read_only_fields = ['id']


# 🔹 Product Attribute
class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    value = AttributeValueSerializer(read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['id', 'attribute', 'value']
        read_only_fields = ['id', 'attribute', 'value']


# 🔹 Product Images
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']
        read_only_fields = ['id']


# 🔹 Product Variants
class ProductVariantSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()
    formatted_original_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'size', 'color', 'stock', 'price',
            'original_price', 'final_price', 'formatted_price',
            'formatted_original_price', 'discount_percentage',
        ]
        read_only_fields = ['id', 'size', 'color', 'sku']

    def get_discount_percentage(self, obj):
        percentage = obj.discount_percentage()
        return f"{percentage}%"

    def get_final_price(self, obj):
        return f"KSh {obj.price:.2f}"

    def get_formatted_price(self, obj):
        return f"KSh {obj.price:.2f}"

    def get_formatted_original_price(self, obj):
        if obj.original_price:
            return f"KSh {obj.original_price:.2f}"
        return None


# 🔹 Product
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = [
            'id', 'slug', 'created_at', 'category',
            'images', 'variants', 'attributes', 'sku', 'reviews',
        ]

    def get_gallery(self, obj):
        return [image.image.url for image in obj.images.all()]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            avg = reviews.aggregate(Avg('rating'))['rating__avg']
            return round(avg, 1)
        return None

    def get_review_count(self, obj):
        return obj.reviews.count()
