import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_group_name = self.scope['url_route']['kwargs']['room_name']

		if self.scope.get("user"):
			await self.channel_layer.group_add(
					self.room_group_name, 
					self.channel_name
					)
			await self.accept()
		else:
			await send({"type": "websocket.close", "code": 4000})

		# self.room_group_name = self.scope['url_route']['kwargs']['room_name']
		# await self.channel_layer.group_add(
		# 	self.room_group_name ,
		# 	self.channel_name
		# )
		# await self.accept()

	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.room_group_name , 
			self.channel_layer 
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		sender = self.scope.get("user")
		message = text_data_json["message"]
		# save to database
		
		await self.channel_layer.group_send(
			self.room_group_name,{
				"type" : "send_message" ,
				"message" : message,
				"sender" : sender.username
			})

	async def send_message(self , event) : 
		message = event["message"]
		await self.send(text_data = json.dumps({
										"message": message,
										"sender": sender
										}))
