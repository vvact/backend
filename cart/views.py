from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product, ProductVariant

class CartViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_cart(self, request):
        # 🔑 Ensure session exists
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            session_key=None if request.user.is_authenticated else session_key
        )
        return cart

    def list(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_cart(self):
        request = self.request
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            session_key=None if request.user.is_authenticated else session_key
        )
        return cart

    def get_queryset(self):
        return self.get_cart().items.all()

    def get_serializer_context(self):
        return {'cart': self.get_cart()}
