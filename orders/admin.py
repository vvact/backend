from django.contrib import admin

# Register your models here.
#orders/admin.py
from .models import Order, OrderItem
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'created_at')
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__status',)
# This file registers the Order and OrderItem models with the Django admin site,
# allowing for management of orders and their items through the admin interface.
