from django.urls import path
from .views import (
    OrderCreateView, OrderDetailView, MyOrdersView,
    UpdateOrderStatusView, NeighborhoodListView
)

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create-order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('my/', MyOrdersView.as_view(), name='my-orders'),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('neighborhoods/', NeighborhoodListView.as_view(), name='neighborhood-list'),
]


import logging
logger = logging.getLogger(__name__)

def create(self, validated_data):
    logger.debug("Validated Order Data: %s", validated_data)
