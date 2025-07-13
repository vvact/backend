from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem, Neighborhood
from products.models import Product
from django.db import transaction


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = ['id', 'name']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        read_only_fields = ['price']  # ✅ Prevent clients from setting price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'email', 'phone_number',
            'neighborhood', 'specific_address', 'notes',
            'total', 'status', 'items', 'created_at'
        ]
        read_only_fields = ['user', 'status', 'created_at', 'total']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = (
            self.context['request'].user
            if self.context.get('request') and self.context['request'].user.is_authenticated
            else None
        )

        with transaction.atomic():
            # Validate stock first
            for item in items_data:
                product = Product.objects.select_for_update().get(id=item['product'].id)
                if product.stock < item['quantity']:
                    raise ValidationError(f"Insufficient stock for product: {product.name}")

            # Calculate total price
            total = sum(item['quantity'] * item['product'].price for item in items_data)

            # Create order
            order = Order.objects.create(user=user, total=total, **validated_data)

            # Create order items and deduct stock
            for item in items_data:
                product = Product.objects.select_for_update().get(id=item['product'].id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price  # ✅ Set price based on current product price
                )
                product.stock -= item['quantity']
                product.save()

        return order
