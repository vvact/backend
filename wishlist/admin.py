from django.contrib import admin

# Register your models here.
#wishlist/admin.py
from .models import Wishlist
admin.site.register(Wishlist)
# This will allow the Wishlist model to be managed through the Django admin interface.
