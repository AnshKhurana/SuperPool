from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .exceptions import ClientError
from .utils import get_service_or_error
from pool.models import FoodService, Message
from datetime import datetime


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.

    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.accept()
        # Store which services the user has joined on this connection
        self.services = set()

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        try:
            if command == "join":
                # Make them join the service
                await self.join_service(content["service"])
            elif command == "leave":
                # Leave the service
                await self.leave_service(content["service"])
            elif command == "send":
                await self.send_service(content["service"], content["message"])
        except ClientError as e:
            # Catch any errors and send it back
            await self.send_json({"error": e.code})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the services we are still in
        for service_id in list(self.services):
            try:
                await self.leave_service(service_id)
            except ClientError:
                pass

    ##### Command helper methods called by receive_json

    async def join_service(self, service_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        service = await get_service_or_error(service_id, self.scope["user"])
        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_SERVICES:
            await self.channel_layer.group_send(
                service.group_name,
                {
                    "type": "chat.join",
                    "service_id": service_id,
                    "username": self.scope["user"].username,
                }
            )
        # Store that we're in the service
        self.services.add(service_id)
        # Add them to the group so they get service messages
        await self.channel_layer.group_add(
            service.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the service
        await self.send_json({
            "join": str(service.id),
            "description": service.description,
        })

        # await self.send_service(service_id, 'default_message')
        messages = Message.objects.filter(service__id=service_id)
        for message in messages:
            event = {"service_id": service_id, "username": message.user.username, "message": message.content}
            await self.chat_message(event, init=True)

    async def leave_service(self, service_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        service = await get_service_or_error(service_id, self.scope["user"])
        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_SERVICES:
            await self.channel_layer.group_send(
                service.group_name,
                {
                    "type": "chat.leave",
                    "service_id": service_id,
                    "username": self.scope["user"].username,
                }
            )
        # Remove that we're in the service
        self.services.discard(service_id)
        # Remove them from the group so they no longer get service messages
        await self.channel_layer.group_discard(
            service.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the service
        await self.send_json({
            "leave": str(service.id),
        })

    async def send_service(self, service_id, message):
        """
        Called by receive_json when someone sends a message to a service.
        """
        # print('sending...')
        # print(service_id)
        # print(self.scope["user"].username)
        # print(message)
        message_instance = Message(timestamp=datetime.now(), content=message, service=FoodService.objects.get(id=service_id), user=self.scope["user"])
        message_instance.save()
        # Check they are in this service
        if service_id not in self.services:
            raise ClientError("service_ACCESS_DENIED")
        # Get the service and send to the group about it
        service = await get_service_or_error(service_id, self.scope["user"])
        await self.channel_layer.group_send(
            service.group_name,
            {
                "type": "chat.message",
                "service_id": service_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client

        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "service": event["service_id"],
                "username": event["username"],
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "service": event["service_id"],
                "username": event["username"],
            },
        )

    async def chat_message(self, event, init=False):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        # print(event["username"])
        # print(self.scope['user'].email)
        if init:
            await self.send_json(
                {
                    "msg_type": settings.MSG_TYPE_MESSAGE,
                    "service": event["service_id"],
                    "username": event["username"],
                    "message": event["message"],
                },
            )
        else:
            await self.send_json(
                {
                    "msg_type": settings.MSG_TYPE_MESSAGE,
                    "service": event["service_id"],
                    "username": event["username"],
                    "message": event["message"],
                },
            )
