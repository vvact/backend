from rest_framework import serializers
from products.models import (
    Product, Category, ProductImage,
    ProductVariant, Size, Color,
    Attribute, AttributeValue,
    ProductAttribute
)

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

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'stock', 'additional_price']
        read_only_fields = ['id', 'size', 'color']

# 🔹 Product
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'price', 'stock', 'main_image', 'created_at',
            'category', 'images', 'variants', 'attributes'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'category', 'images', 'variants', 'attributes']
