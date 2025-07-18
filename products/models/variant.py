from django.db import models
from .product import Product
from .color import Color
from .size import Size
import uuid

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/variants/', blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.color or ''} {self.size or ''}".strip()

    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(100 * (self.original_price - self.price) / self.original_price)
        return 0


    class Meta:
        verbose_name_plural = "ProductVariants"
