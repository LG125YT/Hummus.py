from .role import Role, Permissions
from .file import File, Icon
from .message import Message
from .embed import Embed

from typing import *
import contextlib
import asyncio

class PermissionOverwrite:
	def __init__(self,data):
		from .user import User, Member
		if type(data) == dict:
			self.id:str = data['id']
			self.type:str = data['type']
			self.allow:Permissions = Permissions(data['allow'])
			self.deny:Permissions = Permissions(data['deny'])
		if type(data) == Role:
			self.id:str = data.id
			self.type:str = "role"
			self.allow:Permissions = data.permissions
			self.deny:Permissions = Permissions(0)
		if type(data) == Member or type(data) == User:
			self.id:str = data.id
			self.type:str = "member"
			self.allow:Permissions = Permissions(0)
			self.deny:Permissions = Permissions(0)

	async def hasPermission(self,perm:str) -> Union[bool,None]:
		allow = await self.allow.hasPermission(perm)
		deny = await self.deny.hasPermission(perm)
		if allow == deny == False:
			return None
		elif allow == True:
			return True
		elif deny == True:
			return False

	def toDict(self):
		self.allow.update()
		self.deny.update()
		return {"id":self.id,"type":self.type,"allow":self.allow.value,"deny":self.deny.value}

class InvitePartialGuild:
	def __init__(self,data,instance):
		self.instance = instance
		self.id:str = data['id']
		self.name:str = data['name']
		self.splash:Union[str,None] = data.get('splash')
		self.icon:Icon = Icon(data,"icon",instance)
		self.owner_id:str = data['owner_id']
		self.features:list[str] = data['features']

	async def getMore(self) -> 'PartialGuild':
		return await self.instance.http.get_guild(self.id)

	async def getFull(self) -> 'Guild':
		for guild in self.instance.guilds:
			if guild.id == self.id:
				return guild
		raise Exception("Client is not in guild, please use the \"getMore\" function to get guild info instead. (will not include channels, emojis, roles, and members/membercount)")

	async def leave(self) -> None:
		return await self.instance.http.leave_guild(self.id)

	async def delete(self) -> None:
		return await self.instance.http.delete_guild(self.id)

	async def kick(self,id:str,reason:Union[str,None]=None) -> None:
		return await self.instance.http.kick(self.id,id,reason)

	async def getBans(self) -> List['Ban']:
		return await self.instance.http.get_bans(self.id)

	async def banMember(self,user_id:str,reason:Union[str,None]=None,delete_message_days:int=0) -> None:
		return await self.instance.http.ban(self.id,user_id,reason,delete_message_days)

	async def unbanMember(self,user_id:str) -> None:
		return await self.instance.http.unban(self.id,user_id)

	async def updateMember(self,id:str,nick:Union[str,None]=None,roles:Union[List[Union[Role,str]],None]=None)-> None:
		return await self.instance.http.update_guild_member(self.id,id,nick,roles)

	async def update(self,name:Union[str,None]=None,icon:Union[File,None]=None) -> 'PartialGuild':
		return await self.instance.http.update_guild(self.id,name,icon)

	async def nickSelf(self,nick:str=""):
		return await self.instance.http.nick_self(self.id,nick)

	async def getChannel(self,channel_id:str) -> 'Channel':
		return await self.instance.http.get_channel(channel_id)

	async def updateChannelPostion(self,channel_id:str,position:int) -> List['Channel']:
		return await self.instance.http.update_channel_position(self.id,channel_id,position)

	async def updateChannel(self,id:str,name:Union[str,None]=None,topic:Union[str,None]=None,nsfw:Union[bool,None]=None,bitrate:Union[int,None]=None,user_limit:Union[int,None]=None) -> 'Channel':
		return await self.instance.http.update_channel(self.id,id,name,topic,nsfw,bitrate,user_limit)

	async def createChannel(self,name:str,type:int=0,bitrate:Union[int,None]=None,user_limit:Union[int,None]=None,permission_overwrites:Union[List[PermissionOverwrite],None]=None,nsfw:bool=False) -> 'Channel':
		return await self.instance.http.create_channel(self.id,name,type,bitrate,user_limit,permission_overwrites,nsfw)

	async def deleteChannel(self,id:str) -> None:
		return await self.instance.http.delete_channel(id)

	async def createRole(self) -> Role:
		return await self.instance.http.create_role(self.id)

	async def setRolePostion(self,id:str,position:int) -> List[Role]:
		return await self.instance.http.set_role_position(self.id,id,position)

	async def editRole(self,guild_id:str,id:str,name:Union[str,None]=None,permissions:Union[Permissions,int,None]=None,color:Union[int,None]=None,hoist:Union[bool,None]=None,mentionable:Union[bool,None]=None) -> Role:
		return await self.instance.http.edit_role(guild_id,id,name,permissions,color,hoist,mentionable)
	
	async def deleteRole(self,id:str) -> None:
		return await self.instance.http.delete_role(self.id,id)

	async def getEmojis(self) -> List['Emoji']:
		return await self.instance.http.get_emojis(self.id)

	async def getEmoji(self,id:str) -> 'Emoji':
		return await self.instance.http.get_emoji(self.id,id)

	async def createEmoji(self,name:str,image:File) -> 'Emoji':
		return await self.instance.http.create_emoji(self.id,name,image)

	async def editEmoji(self,id:str,name:str) -> 'Emoji':
		return await self.instance.http.edit_emoji(self.id,id,name)

	async def deleteEmoji(self,id:str) -> None:
		return await self.instance.http.delete_emoji(self.id,id)
	
	async def createInvite(self) -> 'Invite':
		return await self.instance.http.create_channel_invite(self.id) #default channel id is the same as guild id

	async def getChannelInvites(self,id:str) -> List['Invite']:
		return await self.instance.http.get_channel_invites(id)

class Typing:
	def __init__(self,channel):
		self._isTyping = False
		self.channel = channel

	async def doTypingAction(self):
		while self._isTyping:
			await self.channel.startTyping()
			await asyncio.sleep(10)

	async def __aenter__(self):
		self._isTyping = True
		self.background_task = asyncio.create_task(self.doTypingAction())
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		self._isTyping = False
		if self.background_task:
			self.background_task.cancel()
			with contextlib.suppress(asyncio.CancelledError):
				await self.background_task

class PartialChannel:
	def __init__(self,data,guild_id,instance):
		self.instance = instance
		self.guild_id:Union[str,None] = guild_id
		self.id:str = data['id']
		self.type:int = data['type']
		self.name:Union[str,None] = data.get('name') #text and gc
		self.typing:Typing = Typing(self)

	async def getFull(self) -> 'Channel':
		return await self.instance.http.get_channel(self.id)

	async def getOverwrites(self) -> List[PermissionOverwrite]:
		for guild in self.instance.guilds:
			if guild.id == self.guild_id:
				for channel in guild.channels:
					if channel.id == self.id:
						return channel.overwrites
		raise Exception("Client is not in a guild that contains this channel!")

	async def startTyping(self) -> None:
		return await self.instance.http.start_typing(self.id)

	async def bulkDelete(self,messages:List[Union[Message,str]]) -> None:
		return await self.instance.http.bulk_delete(self.id,messages)

	async def sendMessage(self,message:str="",embeds:List[Embed]=[],file:Union[File,None]=None,tts:bool=False) -> Message:
		return await self.instance.http.send_message(self.id,message,embeds,file,tts)

	async def getMessages(self,limit:int=50) -> List[Message]:
		return await self.instance.http.get_messages(self.id,limit)

	async def getPins(self) -> List[Message]:
		return await self.instance.http.get_channel_pins(self.id)

	async def pinMessage(self,message:Union[Message,str]) -> None:
		message = message.id if type(message) == Message else message
		return await self.instance.http.pin_message(self.id,message)

	async def unpinMessage(self,message:Union[Message,str]) -> None:
		message = message.id if type(message) == Message else message
		return await self.instance.http.unpin_message(self.id,message)

	async def getInvites(self) -> List['Invite']:
		return await self.instance.http.get_channel_invites(self.id)

	async def createInvite(self,max_age:Union[int,None]=None,max_uses:Union[int,None]=None,temporary:Union[bool,None]=None,unique:Union[bool,None]=None) -> 'Invite':
		return await self.instance.http.create_channel_invite(self.id,max_age,max_uses,temporary,unique)

	async def updatePosition(self,position:int) -> List['Channel']:
		return await self.instance.http.update_channel_position(self.guild_id,self.id,position)

	async def updateChannel(self,name:Union[str,None]=None,position:Union[int,None]=None,topic:Union[str,None]=None,nsfw:Union[bool,None]=None,bitrate:Union[int,None]=None,user_limit:Union[int,None]=None) -> 'Channel':
		if not name:
			name = self.name
		return await self.instance.http.update_channel(self.id,name,position,topic,nsfw,bitrate,user_limit)

	async def addOverwrite(self,overwrite:PermissionOverwrite) -> None:
		return await self.instance.http.add_channel_overwrite(self.id,overwrite)

	async def deleteOverwrite(self,target:str) -> None:
		return await self.instance.http.delete_channel_overwrite(self.id,target)

	async def delete(self) -> None:
		return await self.instance.http.delete_channel(self.id)

class Invite:
	def __init__(self,data,instance,has_metadata:bool=False):
		from .user import User
		self.instance = instance
		self.url:str = self.instance.base_url.replace("/api","").replace("/v6","") + data['code']
		self.code:str = data['code']
		self.guild:InvitePartialGuild = InvitePartialGuild(data['guild'],instance)
		self.channel:PartialChannel = PartialChannel(data['channel'],data['guild']['id'],instance)
		self.approximate_presence_count:Union[int,None] = data.get('approximate_presence_count')
		self.approximate_member_count:Union[int,None] = data.get('approximate_member_count')
		self.has_metadata:bool = has_metadata
		self.created_at:Union[str,None] = data.get('created_at')
		self.max_uses:Union[int,None] = data.get('max_uses')
		self.max_age:Union[int,None] = data.get('max_age')
		self.temporary:Union[bool,None] = data.get('temporary')
		self.uses:Union[int,None] = data.get('uses')
		self.inviter:User = User(data['inviter'],instance,self.guild.id)

	async def delete(self) -> None:
		return await self.instance.http.delete_invite(self.code)

class PartialGuild(InvitePartialGuild):
	def __init__(self,data,instance):
		super().__init__(data,instance)
		self.region = data['region']
		self.roles = [Role(role,self.id,instance) for role in data['roles']]
		self.emojis = [Emoji(emoji,instance) for emoji in data['emojis']]
		self.voice_states = data['voice_states']
		self.afk_timeout = data['afk_timeout']

	async def getMore(self) -> 'PartialGuild': #not needed as it will just return this object again
		raise Exception("PartialGuild.getMore() is not needed as it will just return this object again.")

class Channel(PartialChannel):
	def __init__(self,data,instance):
		from .user import User
		super().__init__(data,data['guild_id'],instance)
		self.instance = instance
		self.guild_id:Union[str,None] = data['guild_id'] #always exists
		self.last_message_id:Union[str,None] = data.get('last_message_id') #text-based
		self.topic:Union[str,None] = data.get('topic') #text
		self.nsfw:Union[bool,None] = bool(data.get('nsfw')) #text
		self.bitrate:Union[int,None] = data.get('bitrate') #voice
		self.user_limit:Union[int,None] = data.get('user_limit') #voice
		self.owner_id:Union[str,None] = data.get('owner_id') #gc
		self.application_id:Union[str,None] = data.get('application_id') #gc
		if self.guild_id:
			self.permission_overwrites:list[PermissionOverwrite] = [PermissionOverwrite(overwrite) for overwrite in data['permission_overwrites']]
			self.position:int = data['position']
		if data['type'] == 3:
			self.recipients:list[User] = [User(data,instance) for data in data['recipients']]
			self.icon:Icon = Icon(data,"icon",self.instance)
		if data['type'] == 1:
			self.recipients:list[User] = [User(data,instance) for data in data['recipients']]

	async def getFull(self) -> 'Channel': #not needed as it will just return this object again
		raise Exception("Channel.getFull() is not needed as it will just return this object again.")

	def toDict(self):
		if self.type == 0:
			return {"name":self.name,"permission_overwrites":self.permission_overwrites,"position":self.position,"topic":self.topic,"nsfw":self.nsfw,"last_message_id":self.last_message_id,"type":self.type,"id":self.id,"guild_id":self.guild_id}
		elif self.type == 2:
			return {"bitrate":self.bitrate,"name":self.name,"permission_overwrites":self.permission_overwrites,"position":self.position,"user_limit":self.user_limit,"type":self.type,"id":self.id,"guild_id":self.guild_id}

	async def updateChannel(self,name:Union[str,None]=None,position:Union[int,None]=None,topic:Union[str,None]="",nsfw:Union[bool,None]=None,bitrate:Union[int,None]=None,user_limit:Union[int,None]=None) -> 'Channel': #type:ignore | fills in info not available in a PartialChannel object
		if not name:
			name = self.name
		if not position:
			position = self.position
		if self.type == 0:
			if topic == "":
				topic = self.topic
			if nsfw == None:
				nsfw = self.nsfw
		if self.type == 2:
			if not bitrate:
				bitrate = self.bitrate
			if not user_limit:
				user_limit = self.user_limit
		return await self.instance.http.update_channel(self.id,name,position,topic,nsfw,bitrate,user_limit)

class Emoji:
	def __init__(self,data,instance):
		from .user import User
		self.instance = instance
		self.id:str = data['id']
		self.name:str = data['name']
		self.guild_id:str = data.get('guild_id')
		self.roles:list = data['roles']
		self.user:User = User(data['user'],instance,self.guild_id)
		self.require_colons:bool = data['require_colons']
		self.managed:bool = data['managed']
		self.allNamesString:str = data['allNamesString']

	async def edit(self,name) -> 'Emoji':
		return await self.instance.http.edit_emoji(self.guild_id,self.id,name)

	async def delete(self) -> None:
		return await self.instance.http.delete_emoji(self.guild_id,self.id)

	def toDict(self):
		return {"id":self.id,"name":self.name,"roles":self.roles,"user":self.user.toDict(),"require_colons":self.require_colons,"managed":self.managed,"allNamesString":self.allNamesString}

class Guild(PartialGuild):
	def __init__(self,guild,instance):
		from .user import Member, Presence
		super().__init__(guild,instance)
		self.instance = instance
		self.channels:list[Channel] = [Channel(channel,instance) for channel in guild['channels']]
		self.members:list[Member] = [Member(member,self.id,instance,self.roles) for member in guild['members']]
		self.owner:Member = None #type:ignore
		for member in self.members:
			if member.id == self.owner_id:
				self.owner = member
		self.large:bool = guild['large']
		self.member_count:int = guild['member_count']
		self.presences:list[Presence] = [Presence(presence,self.id,instance) for presence in guild['presences']]
		self.unavailable:Union[bool,None] = guild.get('unavailable') #nonexistent on guild join mid-session

	async def getFull(self) -> 'Guild': #not needed as it will just return this object again
		raise Exception("Guild.getFull() is not needed as it will just return this object again.")

	async def getClientMember(self):
		for member in self.members:
			if member.id == self.instance.state.user.id:
				return member
		raise Exception("Client is not in this guild!")

	async def getMember(self,id):
		for member in self.members:
			if id == member.id:
				return member
		raise Exception("Could not find member in guild!")

	async def getRole(self,id) -> Role:
		for role in self.roles:
			if id == role.id:
				return role
		raise Exception("Could not find role in guild!")

	def _update_data(self,guild:PartialGuild):
		self.name = guild.name
		self.region = guild.region
		self.icon = guild.icon
		self.owner_id = guild.owner_id
		self.afk_timeout = guild.afk_timeout
		self.features = guild.features
		self.voice_states = guild.voice_states
		self.roles = guild.roles
		self.emojis = guild.emojis

	def toDict(self):
		return {"channels":[channel.toDict() for channel in self.channels], "emojis":[emoji.toDict() for emoji in self.emojis], "roles":[role.toDict() for role in self.roles], "members":[member.toDict() for member in self.members], "large":self.large, "member_count":self.member_count, "presences":[presence.toDict() for presence in self.presences],"unavailable":self.unavailable}

class Ban:
	def __init__(self,data,guild_id,instance):
		from .user import User
		self.instance = instance
		self.guild_id:str = guild_id
		self.reason:Union[str,None] = data['reason']
		self.user:User = User(data['user'],instance)

	async def revoke(self) -> None:
		return await self.instance.http.unban(self.guild_id,self.user.id)
