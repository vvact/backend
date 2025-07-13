from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)  # prevent frontend from submitting price

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")

        if product.stock < quantity:
            raise serializers.ValidationError(
                f"Only {product.stock} item(s) available for '{product.name}'."
            )

        return data

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'address', 'phone', 'status', 'created_at', 'items']
        read_only_fields = ['id', 'status', 'created_at', 'user']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None

        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)

            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']

                # Extra stock check (in case frontend skips it)
                if product.stock < quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}. Only {product.stock} left."
                    )

                # Deduct stock and save product
                product.stock -= quantity
                product.save()

                # Create order item with actual product price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

        return order
