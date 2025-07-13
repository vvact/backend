from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer


# orders/views.py

# This file contains views for handling orders in an e-commerce application.

# 0. View all orders
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 1. Create an order
class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]  # Allow guest or authenticated

# 2. View a specific order
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 3. View all orders by the logged-in user
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# 4. Update order status (e.g., mark as paid)
class UpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Or IsAdminUser if admin-only

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            new_status = request.data.get('status')
            if new_status not in dict(Order.STATUS_CHOICES):
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

            order.status = new_status
            order.save()
            return Response({'message': 'Order status updated'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
