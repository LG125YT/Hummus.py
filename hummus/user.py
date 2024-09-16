from .guild import PartialGuild,Channel
from .role import Role, Permissions
from .file import Icon

from typing import *

class Profile:
	def __init__(self,data,instance):
		self.instance = instance
		self.connected_accounts:list = data['connected_accounts']
		self.relationships:list[User] = [User(user,instance) for user in data['relationships']]
		self.mutual_guilds:list[PartialGuild] = [PartialGuild(guild,instance) for guild in data['mutual_guilds']]
		self.premium_since:str = data['premium_since']
		self.user:User = User(data['user'],instance)

	async def send_friend_request(self) -> None:
		return await self.instance.add_friend(self.user.id)

class Member:
	def __init__(self,data,guild_id,instance,roles=None):
		self.instance = instance
		self.guild_id:str = guild_id
		self.id:str = data['id']
		self.mention:str = f"<@{data['id']}>"
		self.nick:str = data['nick']
		self.roles:list[Role] = []
		if roles:
			for role in roles:
				if role.id in data['roles'] or role.id == guild_id:
					self.roles.append(role)
		else:
			for guild in instance.guilds:
				if guild.id == guild_id:
					for role in guild.roles:
						if role.id in data['roles'] or role.id == guild_id:
							self.roles.append(role)
		self.joined_at:str = data['joined_at']
		self.deaf:bool = data['deaf']
		self.mute:bool = data['mute']
		self.user:User = User(data['user'],instance,guild_id)
		self.permissions = Permissions()
		for role in self.roles:
			perms = role.permissions.get_dict()
			self.permissions.update(**perms)

	async def hasPermission(self,perm:str) -> bool:
		for role in self.roles:
			if await role.hasPermission(perm):
				return True
		for guild in self.instance.guilds:
			if guild.id == self.guild_id and guild.owner_id == self.id:
				return True
		return False

	async def hasChannelPermission(self,channel:Channel,permission:str) -> bool:
		if await self.hasPermission("administrator"):
			return True
		if type(channel) == "str": #in case someone does a thingy, also setting initial type to union will redline a bunch of stuff
			for guild in self.instance.guilds:
				if guild.id == self.guild_id:
					for c in guild.channels:
						if c.id == channel:
							channel = c
							break
					break
		for overwrite in channel.permission_overwrites:
			if overwrite.id == self.id:
				perm = await overwrite.hasPermission(permission)
				if perm is None:
					break
				elif perm:
					return True
				elif not perm:
					return False
		for role in self.roles:
			if await role.hasChannelPermission(channel,permission):
				return True
		return False

	async def canTarget(self,user:'Member') -> bool:
		highest = 0
		for role in self.roles:
			if highest < role.position:
				highest = role.position
		for guild in self.instance.guilds:
			if guild.id == self.guild_id:
				if guild.owner_id == self.id:
					return True
				elif guild.owner_id == user.id:
					return False
		target_highest = 0
		for role in user.roles:
			if target_highest < role.position:
				target_highest = role.position
		return highest > target_highest

	async def send_friend_request(self) -> None:
		return await self.instance.add_friend(self.id)

	def toDict(self):
		return {"id":self.id, "nick":self.nick, "roles":self.roles,"joined_at":self.joined_at, "deaf":self.deaf, "mute":self.mute,"user":self.user.toDict()}

	async def ban(self,reason:Union[str,None]=None,delete_message_days:int=0) -> None:
		return await self.instance.http.ban(self.guild_id,self.id,reason,delete_message_days)

	async def unban(self) -> None:
		return await self.instance.http.unban(self.guild_id,self.id)

	async def setRoles(self,roles:List[Union[Role,str]]) -> None:
		roles = [role.id if type(role) == Role else role for role in roles]
		return await self.instance.http.update_guild_member(self.guild_id,self.id,roles=roles)

	async def removeRoles(self,roles:List[Union[Role,str]]):
		temp = [role.id for role in self.roles]
		for role in roles:
			if type(role) == Role:
				temp.remove(role.id)
			else:
				temp.remove(role)
		roles = temp
		return await self.instance.http.update_guild_member(self.guild_id,self.id,roles=roles)

	async def addRoles(self,roles:List[Union[Role,str]]) -> None:
		temp = [role.id if type(role) == Role else role for role in self.roles]
		roles = [role.id if type(role) == Role else role for role in roles]
		for role in roles:
			temp.append(role)
		roles = temp
		return await self.instance.http.update_guild_member(self.guild_id,self.id,roles=roles)

	async def kick(self,reason:Union[str,None]=None) -> None:
		return await self.instance.http.kick(self.guild_id,self.id,reason)

	async def setNick(self,nick:str) -> None:
		return await self.instance.http.update_guild_member(self.guild_id,self.id,nick=nick)

class Presence:
	def __init__(self,data,guild_id,instance):
		self.instance = instance
		self.guild_id:Union[str,None] = guild_id
		self.game:str = data.get('game')
		self.status:str = data['status']
		self.user:User = User(data['user'],instance,guild_id)

	def toDict(self):
		return {"game":self.game,"status":self.status,"user":self.user.toDict()}

class User:
	def __init__(self,data,instance,guild_id=None):
		self.instance = instance
		self.guild_id:Union[str,None] = guild_id
		self.id:str = data['id']
		self.username:str = data['username']
		self.discriminator:str = data['discriminator']
		self.mention:str = f"<@{data['id']}>"
		self.avatar:Icon = Icon(data,"avatar",self.instance,True)
		self.bot:bool = data.get('bot')

	async def send_friend_request(self) -> None:
		return await self.instance.add_friend(self.id)

	async def getProfile(self) -> Profile:
		return await self.instance.http.get_user_profile(self.id)

	async def getGuildMember(self,guild_id:Union[str,None]=None) -> Member:
		guild_id = guild_id if guild_id else self.guild_id
		if not guild_id:
			raise Exception("This user was not found in a guild.")
		for guild in self.instance.guilds:
			if guild.id == guild_id:
				for member in guild.members:
					if member.id == self.id:
						return member
		raise Exception("Client is not in a guild with the user!")

	def toDict(self):
		return {"id":self.id,"username":self.username,"discriminator":self.discriminator,"mention":self.mention,"avatar":self.avatar.url,"bot":self.bot}

	async def ban(self,reason:Union[str,None]=None,delete_message_days:int=0) -> None:
		if not self.guild_id:
			raise Exception("This user was not found in a guild.")
		return await self.instance.http.ban(self.guild_id,self.id,reason,delete_message_days)

	async def unban(self) -> None:
		if not self.guild_id:
			raise Exception("This user was not found in a guild.")
		return await self.instance.http.unban(self.guild_id,self.id)

	async def setRoles(self,roles:List[Union[Role,str]]) -> None:
		if not self.guild_id:
			raise Exception("This user was not found in a guild.")
		roles = [role.id if type(role) == Role else role for role in roles]
		return await self.instance.http.update_guild_member(self.guild_id,self.id,roles=roles)

	async def removeRoles(self,roles:List[Union[Role,str]]) -> None:
		if not self.guild_id:
			raise Exception("This user was not found in a guild.")
		temp = await self.getGuildMember()
		temp = [role.id for role in temp.roles]
		for role in roles:
			if type(role) == Role:
				temp.remove(role.id)
			else:
				temp.remove(role)
		roles = temp
		return await self.instance.http.update_guild_member(self.guild_id,self.id,roles=roles)

	async def addRoles(self,roles:List[Union[Role,str]]) -> None:
		if not self.guild_id:
			raise Exception("This user was not found in a guild.")
		temp = await self.getGuildMember()
		temp = [role.id for role in temp.roles]
		for role in roles:
			temp.append(role.id if type(role) == Role else role)
		roles = temp
		return await self.instance.http.update_guild_member(self.guild_id,self.id,roles=roles)

	async def kick(self,reason:Union[str,None]=None) -> None:
		if not self.guild_id:
			raise Exception("This user was not found in a guild.")
		return await self.instance.http.kick(self.guild_id,self.id,reason)

	async def nick(self,nick:str) -> None:
		if not self.guild_id:
			raise Exception("This user was not found in a guild.")
		return await self.instance.http.update_guild_member(self.guild_id,self.id,nick=nick)
