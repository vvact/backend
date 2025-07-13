# orders admin
from django.contrib import admin
from .models import Order, OrderItem
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at',  'status')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__status',)
    raw_id_fields = ('order', 'product')