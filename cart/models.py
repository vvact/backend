from django.db import models
from django.conf import settings
from products.models import ProductVariant, Product

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def grand_total(self):
        # Can add tax/shipping later
        return self.subtotal
    
    def __str__(self):
        return f"Cart ({self.user or self.session_key})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'variant', 'product') 

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        base_price = self.product.price
        extra = self.variant.additional_price if self.variant else 0
        return (base_price + extra) * self.quantity
