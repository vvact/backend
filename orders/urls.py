from django.urls import path
from .views import CreateOrderView, OrderDetailView, MyOrdersView, UpdateOrderStatusView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('my/', MyOrdersView.as_view(), name='my-orders'),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]
# orders/urls.py
# This file defines the URL patterns for the orders app, mapping URLs to their respective views.