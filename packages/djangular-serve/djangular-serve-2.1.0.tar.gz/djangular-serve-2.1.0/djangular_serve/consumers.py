"""
Consumer to manage WebSocket connections for the Djangular-Serve app,
called when the websocket is handshaking as part of initial connection.
"""
import json

from pip._internal.locations import site_packages # noqa

module = "channels"  # django-channels
if module in site_packages:
    try:
        from channels.generic.websocket import AsyncWebsocketConsumer # noqa
    except ModuleNotFoundError:
        print("Please install django_channels: 'pip install django-channels' or 'pip3 install django-channels'")


class ServeConsumer(AsyncWebsocketConsumer):
    """Consumer to manage WebSocket connections for the Djangular-Serve app,
    called when the websocket is handshaking as part of initial connection.
    """

    async def connect(self):
        """Consumer Connect implementation, to validate user status and prevent
        non authenticated user to take advantage from the connection."""
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()

        else:
            # Accept the connection
            await self.channel_layer.group_add("serve", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        """Consumer implementation to leave behind the group at the moment the
        closes the connection."""
        await self.channel_layer.group_discard("serve", self.channel_name)

    async def receive(self, text_data):
        """Receive method implementation to redirect any new message received
        on the websocket to broadcast to all the clients."""
        await self.send(text_data=json.dumps(text_data))
