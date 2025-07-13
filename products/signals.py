from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product

@receiver(pre_save, sender=Product)
def update_in_stock_status(sender, instance, **kwargs):
    instance.in_stock = instance.stock > 0
