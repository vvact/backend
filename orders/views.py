from rest_framework import generics, permissions
from .models import Order, Neighborhood
from .serializers import OrderSerializer, NeighborhoodSerializer


# 🔹 1. Create an Order (supports guests)
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]


# 🔹 2. View a Single Order (by ID)
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# 🔹 3. List All Neighborhoods (for delivery)
class NeighborhoodListView(generics.ListAPIView):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer
    permission_classes = [permissions.AllowAny]


# 🔹 4. Update Order Status (Admin Only)
class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# 🔹 5. List My Orders (Authenticated User Only)
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
