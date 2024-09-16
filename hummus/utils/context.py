from ..guild import Guild,Channel,Typing,Invite
from ..user import User,Member
from ..message import Message
from ..internal import Reply
from ..embed import Embed
from ..file import File

from typing import *

class Context:
	def __init__(self,data,instance):
		from ..http import HTTP
		self.instance = instance
		self.message:Message = data
		self.channel:Channel = data.channel
		self.guild:Union[Guild,None] = data.guild
		self.guild_id:str = data.guild_id
		self.channel_id:str = data.channel_id
		self.author:User = data.author
		self.http:HTTP = instance.http
		self.typing:Typing = Typing(self.channel)

	async def reply(self, content:str="",embeds:List[Embed]=[],file:Union[File,None]=None) -> Message:
		return await self.http.send_message(self.message.channel_id,f"> {self.message.content} \n<@{self.author.id}> {content}",embeds,file,_reply=Reply(self.message))

	async def sendMessage(self, content:str="",embeds:List[Embed]=[],file:Union[File,None]=None) -> Message:
		return await self.http.send_message(self.message.channel_id,content,embeds,file)

	async def startTyping(self) -> None:
		return await self.http.start_typing(self.channel.id)

	async def getPins(self):
		return await self.http.get_channel_pins(self.channel.id)

	async def createInvite(self) -> Invite:
		return await self.http.create_channel_invite(self.channel.id)

	async def getClientMember(self) -> Member:
		if self.guild: #people can use ctx.state.user if they need client user and the received message results to not be in a guild
			return await self.guild.getClientMember()
		raise Exception("Client is not in a guild!")
