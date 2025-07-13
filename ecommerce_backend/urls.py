
from django.contrib import admin
from django.urls import include, path,include
from products.views import CategoryViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static



# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/wishlist/', include('wishlist.urls')),
]
# ✅ Add this block to serve media during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        

