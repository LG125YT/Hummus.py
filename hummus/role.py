from typing import *

class Role:
	def __init__(self,data,guild_id,instance):
		self.instance = instance
		self.guild_id:str = guild_id
		self.id:str = data['id']
		self.name:str = data['name']
		self.color:int = data['color']
		self.permissions:Permissions = Permissions(data['permissions'])
		self.mentionable:bool = data['mentionable']
		self.hoist:bool = data['hoist']
		self.position:int = data['position']

	async def hasPermission(self,permission) -> bool:
		return await self.permissions.hasPermission(permission)

	async def hasChannelPermission(self,channel,permission) -> bool:
		for overwrite in channel.permission_overwrites:
			if overwrite.id == self.id:
				perm = await overwrite.hasPermission(permission)
				if perm is None:
					break
				elif perm:
					return True
				elif not perm:
					return False
		return await self.hasPermission(permission)

	async def edit(self,name=None,permissions=None,color=None,hoist=None,mentionable=None) -> 'Role':
		return await self.instance.http.modify_role(self.guild_id,self.id,name,permissions,color,hoist,mentionable)

	async def updatePosition(self,position) -> List['Role']:
		return await self.instance.http.modify_role_position(self.guild_id,self.id,position)

	async def delete(self) -> None:
		return await self.instance.http.delete_role(self.guild_id,self.id)

	def toDict(self):
		return {"id":self.id, "name":self.name, "color":self.color, "permissions":self.permissions.value, "mentionable":self.mentionable, "hoist":self.hoist,"position":self.position}

class FakeRole: #this is really used to provide a placeholder for top role comparison
	def __init__(self,position):
		self.position = position


#stolen from dpy lol
class Permissions:
	"""Wraps up the Discord permission value.

	Supported operations:

	+-----------+------------------------------------------+
	| Operation |               Description                |
	+===========+==========================================+
	| x == y    | Checks if two permissions are equal.     |
	+-----------+------------------------------------------+
	| x != y    | Checks if two permissions are not equal. |
	+-----------+------------------------------------------+
	| x <= y    | Checks if a permission is a subset       |
	|           | of another permission.                   |
	+-----------+------------------------------------------+
	| x >= y    | Checks if a permission is a superset     |
	|           | of another permission.                   |
	+-----------+------------------------------------------+
	| x < y     | Checks if a permission is a strict       |
	|           | subset of another permission.            |
	+-----------+------------------------------------------+
	| x > y     | Checks if a permission is a strict       |
	|           | superset of another permission.          |
	+-----------+------------------------------------------+
	| hash(x)   | Return the permission's hash.            |
	+-----------+------------------------------------------+
	| iter(x)   | Returns an iterator of (perm, value)     |
	|           | pairs. This allows this class to be used |
	|           | as an iterable in e.g. set/list/dict     |
	|           | constructions.                           |
	+-----------+------------------------------------------+

	The properties provided are two way. You can set and retrieve individual bits using the properties as if they
	were regular bools. This allows you to edit permissions.

	Attributes
	-----------
	value
					The raw value. This value is a bit array field of a 32-bit integer
					representing the currently available permissions. You should query
					permissions via the properties rather than using this raw value.
	"""

	__slots__ = ('value',)
	def __init__(self, obj=0): #modified dpy to accept more objects
		if type(obj) == Role:
			obj.permissions.update()
			permissions = obj.permissions.value
		elif type(obj) == int:
			permissions = obj
		elif type(obj) == str:
			permissions = int(obj)
		elif not obj: #None
			permissions = 0 #creation of a fake role
		else:
			raise TypeError(f'Expected int, Role, str, or None, received {obj.__class__.__name__} instead.')

		self.value = permissions

	async def hasPermission(self,permission) -> bool: #the one function I (LG) actually entirely made
		if self.administrator:
			return True
		from .utils import Exceptions
		try:
			return getattr(self,permission)
		except AttributeError:
			raise Exceptions.InvalidPermission(f"{permission} is not a valid permission!")

	def __eq__(self, other):
		return isinstance(other, Permissions) and self.value == other.value

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.value)

	def __repr__(self):
		return '<Permissions value=%s>' % self.value

	def _perm_iterator(self):
		for attr in dir(self):
			# check if it's a property, because if so it's a permission
			is_property = isinstance(getattr(self.__class__, attr), property)
			if is_property:
				yield (attr, getattr(self, attr))

	def __iter__(self):
		return self._perm_iterator()

	def is_subset(self, other):
		"""Returns True if self has the same or fewer permissions as other."""
		if isinstance(other, Permissions):
			return (self.value & other.value) == self.value
		else:
			raise TypeError("cannot compare {} with {}".format(self.__class__.__name__, other.__class__name))

	def is_superset(self, other):
		"""Returns True if self has the same or more permissions as other."""
		if isinstance(other, Permissions):
			return (self.value | other.value) == self.value
		else:
			raise TypeError("cannot compare {} with {}".format(self.__class__.__name__, other.__class__name))

	def is_strict_subset(self, other):
		"""Returns True if the permissions on other are a strict subset of those on self."""
		return self.is_subset(other) and self != other

	def is_strict_superset(self, other):
		"""Returns True if the permissions on other are a strict superset of those on self."""
		return self.is_superset(other) and self != other

	__le__ = is_subset
	__ge__ = is_superset
	__lt__ = is_strict_subset
	__gt__ = is_strict_superset

	@classmethod
	def none(cls):
		"""A factory method that creates a :class:`Permissions` with all
		permissions set to False."""
		return cls(0)

	@classmethod
	def all(cls):
		"""A factory method that creates a :class:`Permissions` with all
		permissions set to True."""
		return cls(0b01111111111101111111110001111111)

	@classmethod
	def all_channel(cls):
		"""A :class:`Permissions` with all channel-specific permissions set to
		True and the guild-specific ones set to False. The guild-specific
		permissions are currently:

		- manage_guild
		- kick_members
		- ban_members
		- administrator
		- change_nicknames
		- manage_nicknames
		"""
		return cls(0b00110011111101111111110001010001)

	@classmethod
	def general(cls):
		"""A factory method that creates a :class:`Permissions` with all
		"General" permissions from the official Discord UI set to True."""
		return cls(0b01111100000000000000000000111111)

	@classmethod
	def text(cls):
		"""A factory method that creates a :class:`Permissions` with all
		"Text" permissions from the official Discord UI set to True."""
		return cls(0b00000000000001111111110001000000)

	@classmethod
	def voice(cls):
		"""A factory method that creates a :class:`Permissions` with all
		"Voice" permissions from the official Discord UI set to True."""
		return cls(0b00000011111100000000000000000000)
	
	def get_dict(self): #i also made this lol
		vals = {}
		for attr in dir(self):
			val = getattr(self.__class__,attr)
			if isinstance(attr,property) and val:
				vals[attr.__str__] = val
		return vals

	def update(self, **kwargs):
		"""Bulk updates this permission object.

		Allows you to set multiple attributes by using keyword
		arguments. The names must be equivalent to the properties
		listed. Extraneous key/value pairs will be silently ignored.

		Parameters
		------------
		\*\*kwargs
						A list of key/value pairs to bulk update permissions with.
		"""
		for key, value in kwargs.items():
			try:
				is_property = isinstance(getattr(self.__class__, key), property)
			except AttributeError:
				continue

			if is_property:
				setattr(self, key, value)

	def _bit(self, index):
		return bool((self.value >> index) & 1)

	def _set(self, index, value):
		if value == True:
			self.value |= (1 << index)
		elif value == False:
			self.value &= ~(1 << index)
		else:
			raise TypeError('Value to set for Permissions must be a bool.')

	def handle_overwrite(self, allow, deny):
		# Basically this is what's happening here.
		# We have an original bit array, e.g. 1010
		# Then we have another bit array that is 'denied', e.g. 1111
		# And then we have the last one which is 'allowed', e.g. 0101
		# We want original OP denied to end up resulting in
		# whatever is in denied to be set to 0.
		# So 1010 OP 1111 -> 0000
		# Then we take this value and look at the allowed values.
		# And whatever is allowed is set to 1.
		# So 0000 OP2 0101 -> 0101
		# The OP is base  & ~denied.
		# The OP2 is base | allowed.
		self.value = (self.value & ~deny) | allow

	@property
	def create_instant_invite(self):
		"""Returns True if the user can create instant invites."""
		return self._bit(0)

	@create_instant_invite.setter
	def create_instant_invite(self, value):
		self._set(0, value)

	@property
	def kick_members(self):
		"""Returns True if the user can kick users from the guild."""
		return self._bit(1)

	@kick_members.setter
	def kick_members(self, value):
		self._set(1, value)

	@property
	def ban_members(self):
		"""Returns True if a user can ban users from the guild."""
		return self._bit(2)

	@ban_members.setter
	def ban_members(self, value):
		self._set(2, value)

	@property
	def administrator(self):
		"""Returns True if a user is an administrator. This role overrides all other permissions.

		This also bypasses all channel-specific overrides.
		"""
		return self._bit(3)

	@administrator.setter
	def administrator(self, value):
		self._set(3, value)

	@property
	def manage_channels(self):
		"""Returns True if a user can edit, delete, or create channels in the guild.

		This also corresponds to the "manage channel" channel-specific override."""
		return self._bit(4)

	@manage_channels.setter
	def manage_channels(self, value):
		self._set(4, value)

	@property
	def manage_guild(self):
		"""Returns True if a user can edit guild properties."""
		return self._bit(5)

	@manage_guild.setter
	def manage_guild(self, value):
		self._set(5, value)

	@property
	def add_reactions(self):
		"""Returns True if a user can add reactions to messages."""
		return self._bit(6)

	@add_reactions.setter
	def add_reactions(self, value):
		self._set(6, value)

	# 4 unused

	@property
	def read_messages(self):
		"""Returns True if a user can read messages from all or specific text channels."""
		return self._bit(10)

	@read_messages.setter
	def read_messages(self, value):
		self._set(10, value)

	@property
	def send_messages(self):
		"""Returns True if a user can send messages from all or specific text channels."""
		return self._bit(11)

	@send_messages.setter
	def send_messages(self, value):
		self._set(11, value)

	@property
	def send_tts_messages(self):
		"""Returns True if a user can send TTS messages from all or specific text channels."""
		return self._bit(12)

	@send_tts_messages.setter
	def send_tts_messages(self, value):
		self._set(12, value)

	@property
	def manage_messages(self):
		"""Returns True if a user can delete messages from a text channel. Note that there are currently no ways to edit other people's messages."""
		return self._bit(13)

	@manage_messages.setter
	def manage_messages(self, value):
		self._set(13, value)

	@property
	def embed_links(self):
		"""Returns True if a user's messages will automatically be embedded by Discord."""
		return self._bit(14)

	@embed_links.setter
	def embed_links(self, value):
		self._set(14, value)

	@property
	def attach_files(self):
		"""Returns True if a user can send files in their messages."""
		return self._bit(15)

	@attach_files.setter
	def attach_files(self, value):
		self._set(15, value)

	@property
	def read_message_history(self):
		"""Returns True if a user can read a text channel's previous messages."""
		return self._bit(16)

	@read_message_history.setter
	def read_message_history(self, value):
		self._set(16, value)

	@property
	def mention_everyone(self):
		"""Returns True if a user's @everyone will mention everyone in the text channel."""
		return self._bit(17)

	@mention_everyone.setter
	def mention_everyone(self, value):
		self._set(17, value)

	@property
	def external_emojis(self):
		"""Returns True if a user can use emojis from other guilds."""
		return self._bit(18)

	@external_emojis.setter
	def external_emojis(self, value):
		self._set(18, value)

	# 1 unused

	@property
	def connect(self):
		"""Returns True if a user can connect to a voice channel."""
		return self._bit(20)

	@connect.setter
	def connect(self, value):
		self._set(20, value)

	@property
	def speak(self):
		"""Returns True if a user can speak in a voice channel."""
		return self._bit(21)

	@speak.setter
	def speak(self, value):
		self._set(21, value)

	@property
	def mute_members(self):
		"""Returns True if a user can mute other users."""
		return self._bit(22)

	@mute_members.setter
	def mute_members(self, value):
		self._set(22, value)

	@property
	def deafen_members(self):
		"""Returns True if a user can deafen other users."""
		return self._bit(23)

	@deafen_members.setter
	def deafen_members(self, value):
		self._set(23, value)

	@property
	def move_members(self):
		"""Returns True if a user can move users between other voice channels."""
		return self._bit(24)

	@move_members.setter
	def move_members(self, value):
		self._set(24, value)

	@property
	def use_voice_activation(self):
		"""Returns True if a user can use voice activation in voice channels."""
		return self._bit(25)

	@use_voice_activation.setter
	def use_voice_activation(self, value):
		self._set(25, value)

	@property
	def change_nickname(self):
		"""Returns True if a user can change their nickname in the guild."""
		return self._bit(26)

	@change_nickname.setter
	def change_nickname(self, value):
		self._set(26, value)

	@property
	def manage_nicknames(self):
		"""Returns True if a user can change other user's nickname in the guild."""
		return self._bit(27)

	@manage_nicknames.setter
	def manage_nicknames(self, value):
		self._set(27, value)

	@property
	def manage_roles(self):
		"""Returns True if a user can create or edit roles less than their role's position.

		This also corresponds to the "manage permissions" channel-specific override.
		"""
		return self._bit(28)

	@manage_roles.setter
	def manage_roles(self, value):
		self._set(28, value)

	@property
	def manage_webhooks(self):
		"""Returns True if a user can create, edit, or delete webhooks."""
		return self._bit(29)

	@manage_webhooks.setter
	def manage_webhooks(self, value):
		self._set(29, value)

	@property
	def manage_emojis(self):
		"""Returns True if a user can create, edit, or delete emojis."""
		return self._bit(30)

	@manage_emojis.setter
	def manage_emojis(self, value):
		self._set(30, value)
