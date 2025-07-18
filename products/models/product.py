from django.db import models
from .category import Category
from django.utils.text import slugify
import uuid
import string, random

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=20, unique=True, blank=True)  # 👈 NEW
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        if not self.sku:
            self.sku = self.generate_unique_sku()

        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        from django.utils.text import slugify
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def generate_unique_sku(self):
        chars = string.ascii_uppercase + string.digits
        while True:
            code = f"P-{''.join(random.choices(chars, k=3))}"
            if not Product.objects.filter(sku=code).exists():
                return code