import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import products.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("🚀 Loaded custom ASGI application with Channels routing")  # ✅ ADD THIS
print("✅ ASGI file is loading...")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            products.routing.websocket_urlpatterns
        )
    ),
})
