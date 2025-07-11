# cart/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
from django.shortcuts import get_object_or_404

class CartViewSet(viewsets.ViewSet):
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.save()
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart

    def list(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response({"message": "Item added to cart"}, status=201)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        cart = self.get_cart(request)
        item = get_object_or_404(CartItem, cart=cart, id=pk)
        item.delete()
        return Response({"message": "Item removed"}, status=204)

    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, pk=None):
        cart = self.get_cart(request)
        item = get_object_or_404(CartItem, cart=cart, id=pk)
        quantity = int(request.data.get("quantity", 1))
        item.quantity = quantity
        item.save()
        return Response({"message": "Quantity updated"}, status=200)

