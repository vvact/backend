# orders/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def create(self, request):
        user = request.user
        shipping_address = request.data.get('shipping_address')
        phone = request.data.get('phone')

        # Get user's cart
        cart = Cart.objects.filter(user=user).first()
        if not cart or cart.items.count() == 0:
            return Response({"error": "Cart is empty."}, status=400)

        # Calculate total
        total = sum(item.product.price * item.quantity for item in cart.items.all())

        # Create order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            phone=phone,
            total=total,
        )

        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=201)

