from django.contrib import admin
from .models import (
    Product, Category, ProductVariant,
    ProductImage, Size, Color,
    Attribute, AttributeValue,
    ProductAttribute
)

# 🔹 Inline for Variants
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

# 🔹 Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# 🔹 Inline for Product Attributes
class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

# 🔹 Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'base_price', 'stock', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category']
    search_fields = ['name', 'description']
    inlines = [ProductVariantInline, ProductImageInline, ProductAttributeInline]

# 🔹 Register Other Models
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value']
    list_filter = ['attribute']
