# products/utils.py
from django.utils.text import slugify

def unique_slugify(instance, value, slug_field_name='slug'):
    slug = slugify(value)
    ModelClass = instance.__class__
    unique_slug = slug
    num = 1
    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug
