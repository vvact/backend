from rest_framework import serializers
from products.models import Product, ProductVariant
from .models import Cart, CartItem
from products.serializers import ProductSerializer, ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), write_only=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'variant', 'quantity', 'total_price', 'product_id', 'variant_id']
        read_only_fields = ['id', 'total_price']

    def validate(self, data):
        product = data.get('product_id')
        variant = data.get('variant_id', None)
        quantity = data.get('quantity')

        if variant:
            if quantity > variant.stock:
                raise serializers.ValidationError(f"Only {variant.stock} items left in stock for this variant.")
        else:
            if quantity > product.stock:
                raise serializers.ValidationError(f"Only {product.stock} items left in stock.")

        return data

    def create(self, validated_data):
        cart = self.context['cart']
        product = validated_data.pop('product_id')
        variant = validated_data.pop('variant_id', None)
        quantity = validated_data['quantity']

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            new_quantity = item.quantity + quantity
            # ✅ Enforce stock limit on combined quantity
            if variant and new_quantity > variant.stock:
                raise serializers.ValidationError(f"Only {variant.stock} items left in stock.")
            elif not variant and new_quantity > product.stock:
                raise serializers.ValidationError(f"Only {product.stock} items left in stock.")
            item.quantity = new_quantity
            item.save()

        return item

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', instance.quantity)

        if instance.variant:
            if quantity > instance.variant.stock:
                raise serializers.ValidationError(f"Only {instance.variant.stock} items left in stock.")
        else:
            if quantity > instance.product.stock:
                raise serializers.ValidationError(f"Only {instance.product.stock} items left in stock.")

        instance.quantity = quantity
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'created_at', 'items', 'subtotal', 'grand_total']
        read_only_fields = ['id', 'created_at', 'items', 'subtotal', 'grand_total']

    def get_subtotal(self, obj):
        return obj.subtotal

    def get_grand_total(self, obj):
        return obj.grand_total
