from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet

router = DefaultRouter()
router.register(r'', WishlistViewSet, basename='wishlist')  # No 'wishlist' here

urlpatterns = [
    path('', include(router.urls)),
]
# wishlist/urls.py
# This will allow the WishlistViewSet to be accessible at /api/wishlist/