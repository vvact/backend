from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("products", self.channel_name)
        await self.accept()
        print("✅ WebSocket connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("products", self.channel_name)
        print("🔌 WebSocket disconnected")

    async def product_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "product_update",
            "action": event.get("action", "updated"),  # "created" or "updated"
            "product": event["data"]
        }))

    async def product_delete(self, event):
        await self.send(text_data=json.dumps({
            "type": "product_update",
            "action": "deleted",
            "slug": event["slug"]
        }))
