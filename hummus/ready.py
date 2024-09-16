from .guild import Channel,Guild
from .user import User,Presence
from .file import Icon

from typing import *

class Ready:
	def __init__(self,data,instance):
		self.instance = instance
		self.version:int = data.get('v')
		self.user:Self = Self(data['user'],instance)
		self.private_channels:list[Channel] = [Channel(data,instance) for data in data['private_channels']]
		self.guilds_are_unavailable:bool = bool(data['guilds'][0].get('unavailable'))
		if not self.guilds_are_unavailable:
			self.guilds:list[Guild] = [Guild(guild,instance) for guild in data['guilds']]
		else:
			self.guild_ids:list[str] = [guild['id'] for guild in data['guilds']]
		if not data.get('users'):
		    data['users'] = []
		self.users:list[User] = [User(user,instance) for user in data['users']]
		self.presences:list[Presence] = [Presence(data,None,instance) for data in data['presences']]
		self.shard:list[int] = data.get('shard')
		self.session_id:str = data['session_id']
		self._trace:list[str] = data['_trace']
		self.relationships:list[Relationship] = [Relationship(relation,instance) for relation in data['relationships']]
		self.application:Union[Application,None] = None
		if data.get('application'):
			data['application']['discriminator'] = self.user.discriminator
			self.application = Application(data['application'],instance)

class Self(User):
	def __init__(self,data,instance):
		super().__init__(data,instance)
		self.email:str = data['email']
		self.verified:bool = data['verified']
		self.flags:int = data.get('flags')
		self.mfa_enabled:bool = data.get('mfa_enabled')
		self.premium:bool = data['premium']
		self.token:Union[str,None] = data.get('token') #PATCH /users/@me returns this

class Relationship(User):
	def __init__(self,data,instance):
		super().__init__(data['user'],instance)
		self.type:int = data['type']

class Application:
	def __init__(self,data,instance):
		self.instance = instance
		self.id:str = data['id']
		self.name:str = data['name']
		self.description:str = data['description']
		self.icon:Icon = Icon(data,"icon",instance,True)
		self.bot_public:bool = data['bot_public']
		self.bot_require_code_grant:bool = data['bot_require_code_grant']
