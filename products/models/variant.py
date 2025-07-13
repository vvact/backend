from django.db import models
from products.models.product import Product
from products.models.size import Size
from products.models.color import Color

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='variants/', null=True, blank=True)

    def __str__(self):
        details = []
        if self.size:
            details.append(str(self.size))
        if self.color:
            details.append(str(self.color))
        return f"{self.product.name} - {' / '.join(details)}"

    class Meta:
        unique_together = ['product', 'color', 'size']  

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"
