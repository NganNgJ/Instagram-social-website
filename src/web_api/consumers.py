import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name

		if self.scope.get("user"):
			await self.channel_layer.group_add(
					self.room_group_name, 
					self.channel_name
					)
			await self.accept()
		else:
			await send({"type": "websocket.close", "code": 4000})

	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_layer
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		self.user_id = self.scope['user'].id
		message = text_data_json["message"]
		
		#Find room object
		room = await database_sync_to_async(Room.objects.get)(name=self.room_name)

		#Create  new message object
		message = Message(
			content = message,
			sender = self.scope['user'],
			room = room
		)
		
		await self.channel_layer.group_send(
			self.room_group_name,{
				"type" : "send_message",
				"message" : message,
				"user_id" : self.user_id
			})

	async def send_message(self , event) : 
		message = event["message"]
		user_id = event["user_id"]
		await self.send(text_data = json.dumps({
										"message": message,
										"user": user_id
										}))
