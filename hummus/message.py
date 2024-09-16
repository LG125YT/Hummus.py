from .file import File, Attachment
from .embed import Embed

from typing import *

class Message:
	def __init__(self,data,instance,reply:bool=False,reply_content=None,reply_author=None):
		from .internal import makeEmbed
		from .guild import Guild
		from .role import Role
		from .user import User
		if reply:
			self.is_reply:bool = True
			self.original_reply = reply_content
			self.original_author = reply_author
		else:
			self.is_reply:bool = False
		self.instance = instance
		self.guild_id:Union[str,None] = data.get("guild_id")
		self.author:User = User(data['author'],instance,self.guild_id)
		self.content:str = data['content']
		self.channel_id:str = data['channel_id']
		self.mention_roles:list[Role] = []
		self.guild:Union[Guild,None] = None
		self.channel:Channel = None #type:ignore
		if self.guild_id:
			for guild in instance.guilds:
				if self.guild_id == guild.id:
					self.guild = guild
					for channel in guild.channels:
						if data['channel_id'] == channel.id:
							self.channel = channel
					for r in guild.roles:
						if r.id in data['mention_roles']:
							self.mention_roles.append(r)
		else:
			for dm in self.instance.state.private_channels:
				if data['channel_id'] == dm.id:
					self.channel = dm
		self.dm:bool = False
		if not self.guild_id:
			self.dm = True
		self.id:str = data['id']
		self.mentions:list[User] = [User(mention,instance,self.guild_id) for mention in data['mentions']]
		self.attachments:list[Attachment] = [Attachment(attachment,self.instance) for attachment in data['attachments']]
		self.embeds:list[Embed] = makeEmbed(data['embeds'])
		self.edited_timestamp:Union[str,None] = data['edited_timestamp']
		self.pinned:bool = data['pinned']
		self.mention_everyone:bool = data['mention_everyone']
		self.tts:bool = data['tts']
		self.timestamp:str = data['timestamp']
		self.webhook_id:Union[str,None] = data['webhook_id']

	async def typing(self) -> None:
		return await self.instance.http.start_typing(self.channel_id)

	async def delete(self) -> None:
		return await self.instance.http.delete_message(self.channel_id,self.id)

	async def edit(self,content:str) -> 'Message':
		if self.is_reply:
			content = f"> {self.original_reply}\n<@{self.original_author.id}> {content}"
		return await self.instance.http.edit_message(self.channel_id,self.id,content,_reply=self.is_reply,_reply_content=self.original_reply,_reply_author=self.original_author)

	async def send(self,content:str="", embeds:List[Embed]=[],file:Union[File,None]=None) -> 'Message':
		return await self.instance.http.send_message(self.channel_id,content,embeds,file)

	async def reply(self,content:str="",embeds:List[Embed]=[],file:Union[File,None]=None) -> 'Message':
		from .internal import Reply
		return await self.instance.http.send_message(self.channel_id,f"> {self.content}\n<@{self.author.id}> {content}",embeds,file,_reply=Reply(self))

	async def pin(self) -> None:
		return await self.instance.http.pin_message(self.channel_id,self.id)

	async def unpin(self) -> None:
		return await self.instance.http.unpin_message(self.channel_id,self.id)
