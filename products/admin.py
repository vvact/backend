from django.contrib import admin
from .models import (
    Product, ProductVariant, Category,
    Color, Size, Attribute, AttributeValue,
    ProductImage
)
from django.utils.html import mark_safe


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

    

    def thumbnail(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="60" height="60" style="object-fit:cover;" />')
        return "-"
    thumbnail.short_description = 'Preview'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
    def thumbnail(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="60" height="60" style="object-fit:cover;" />')
        return "-"
    thumbnail.short_description = 'Preview'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category',  'created_at']
    search_fields = ['name']
    list_filter = ['category']
    inlines = [ProductVariantInline, ProductImageInline]
    readonly_fields = ['slug']
    exclude = ['sku'] 


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product',  'price', 'original_price', 'stock', 'color', 'size']
    list_filter = ['product', 'color', 'size']
    search_fields = [ 'product__name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    readonly_fields = ['slug']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['value']


