from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Product
from .serializers import ProductSerializer

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "products",
        {
            "type": "product_update",  # Matches handler in consumer
            "action": "created" if created else "updated",
            "data": ProductSerializer(instance).data,
        }
    )

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "products",
        {
            "type": "product_delete",  # Matches handler in consumer
            "slug": instance.slug
        }
    )
