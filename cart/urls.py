# cart/urls.py
from django.urls import path
from .views import CartViewSet

urlpatterns = [
    path('', CartViewSet.as_view({'get': 'list'}), name='cart'),
    path('add/', CartViewSet.as_view({'post': 'add'}), name='cart-add'),
    path('remove/<int:pk>/', CartViewSet.as_view({'delete': 'remove'}), name='cart-remove'),
    path('update/<int:pk>/', CartViewSet.as_view({'patch': 'update_quantity'}), name='cart-update'),
]
