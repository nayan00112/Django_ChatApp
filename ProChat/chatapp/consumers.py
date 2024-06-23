
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

# Not take value from room name routing <str:roomname>

class MySyncCon(SyncConsumer):
    def websocket_connect(self, event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print("==> connect", event)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self, event):
        print("==> Receive",event)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                'type':'chat.message', 
                'message':event['text']
            }
        )

    def chat_message(self, event):
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })
    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name ,
            self.channel_name
        )
        print("==> disconnect", event)
        raise StopConsumer()
    

class MyASyncCon(AsyncConsumer):
    async def websocket_connect(self, event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        self.channel_layer.group_add(self.room_name, self.channel_name)
        print("===> connect", event)

        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("===> Receive as",event)
        await self.channel_layer.group_send(
            self.room_name, 
            {
                'type':'chat.message', 
                'message':event['text']
            }
        )

    async def chat_message(self, event):
        print("====> channel send")
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        print("===> disconnect", event)
        raise StopConsumer()