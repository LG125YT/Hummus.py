from ...guild import Invite, Channel, PermissionOverwrite
from ...message import Message
from ...file import File

from typing import *
import base64

class hChannel:
	def __init__(self,instance):
		self.instance = instance
		self.s = instance.s

	async def create_channel(self,guild_id:str,name:str,type:int=0,bitrate:Union[int,None]=None,user_limit:Union[int,None]=None,permission_overwrites:Union[List[PermissionOverwrite],None]=None,nsfw:bool=False) -> Channel: #parent_id excluded because creating categories doesn't exist
		from ... import HTTPStatus
		data = {"name":name,"type":type,"nsfw":nsfw}
		if bitrate:
			data['bitrate'] = bitrate
		if user_limit:
			data['user_limit'] = user_limit
		if permission_overwrites:
			data['permission_overwrites'] = [{"id":overwrite.id,"type":overwrite.type,"allow":overwrite.allow.value,"deny":overwrite.deny.value} for overwrite in permission_overwrites]
		r = self.s.post(f"{self.instance.base_url}guilds/{guild_id}/channels",json=data)
		s = HTTPStatus(r)
		if s.success:
			return Channel(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

	async def get_channel(self,id:str) -> Channel:
		from ... import HTTPStatus
		r = self.s.get(f"{self.instance.base_url}channels/{id}")
		s = HTTPStatus(r)
		if s.success:
			return Channel(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

	async def get_messages(self,channel_id:str,limit:int=50) -> List[Message]:
		from ... import HTTPStatus
		r = self.s.get(url=f"{self.instance.base_url}channels/{channel_id}/messages/",json={"limit":limit})
		s = HTTPStatus(r)
		if s.success:
			return [Message(message,self.instance) for message in r.json()]
		else:
			raise s.exception(s.reason)

	async def delete_channel(self,id:str) -> None:
		from ... import HTTPStatus
		r = self.s.delete(f"{self.instance.base_url}channels/{id}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def get_channel_pins(self,id:str) -> List[Message]:
		from ... import HTTPStatus, Message
		r = self.s.get(f"{self.instance.base_url}channels/{id}/pins")
		s = HTTPStatus(r)
		if s.success:
			return [Message(message,self.instance) for message in r.json()]
		else:
			raise s.exception(s.reason)

	async def get_channel_invites(self,id:str) -> List[Invite]:
		from ... import HTTPStatus
		r = self.s.get(f"{self.instance.base_url}channels/{id}/invites")
		s = HTTPStatus(r)
		if s.success:
			return [Invite(inv,self.instance,True) for inv in r.json()]
		else:
			raise s.exception(s.reason)

	async def create_channel_invite(self,id:str,max_age:Union[int,None]=None,max_uses:Union[int,None]=None,temporary:bool=False,unique:bool=False) -> Invite:
		from ... import HTTPStatus
		data = {}
		if max_age:
			data['max_age'] = max_age
		if max_uses:
			data['max_uses'] = max_uses
		if temporary:
			data['temporary'] = temporary
		if unique:
			data['unique'] = unique
		r = self.s.post(f"{self.instance.base_url}channels/{id}/invites",json=data)
		s = HTTPStatus(r)
		if s.success:
			return Invite(r.json(),self.instance,True)
		else:
			raise s.exception(s.reason)

	async def get_invite(self,id:str,with_counts:bool=False) -> Invite:
		from ... import HTTPStatus
		r = self.s.get(f"{self.instance.base_url}invites/{id}",json={"with_counts":with_counts})
		s = HTTPStatus(r)
		if s.success:
			return Invite(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

	async def delete_invite(self,id:str) -> None:
		from ... import HTTPStatus
		r = self.s.delete(f"{self.instance.base_url}invites/{id}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def update_channel_position(self,guild_id:str,id:str,position:int) -> List[Channel]:
		from ... import HTTPStatus
		r = self.s.patch(f"{self.instance.base_url}guilds/{guild_id}/channels/",json=[{"id":id,"position":int(position)}])
		s = HTTPStatus(r)
		if s.success:
			return [Channel(channel,self.instance) for channel in r.json()]
		else:
			raise s.exception(s.reason)

	async def update_channel(self,id:str,name:Union[str,None]=None,topic:Union[str,None]=None,nsfw:Union[bool,None]=None,bitrate:Union[int,None]=None,user_limit:Union[int,None]=None) -> Channel:
		data = {}
		if name:
			data['name'] = name
		if topic:
			data['topic'] = topic
		if nsfw:
			data['nsfw'] = nsfw
		if bitrate:
			data['bitrate'] = bitrate
		if user_limit:
			data['user_limit'] = user_limit
		from ... import HTTPStatus
		r = self.s.patch(url=f"{self.instance.base_url}/channels/{id}",json=data)
		s = HTTPStatus(r)
		if s.success:
			return Channel(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

	async def add_channel_overwrite(self,channel_id:str,overwrite:PermissionOverwrite) -> None:
		from ... import HTTPStatus
		if type(overwrite) != PermissionOverwrite:
			raise Exception("Please provide a Permissions Overwrite (PermissionOverwrite) object.")
		overwrite.allow.update()
		overwrite.deny.update()
		data = {"id":overwrite.id,"type":overwrite.type,"allow":overwrite.allow.value,"deny":overwrite.deny.value}
		r = self.s.put(url=f"{self.instance.base_url}channels/{channel_id}/permissions/{overwrite.id}",json=data)
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def delete_channel_overwrite(self,channel_id:str,target:str) -> None:
		from ... import HTTPStatus
		r = self.s.delete(f"{self.instance.base_url}channels/{channel_id}/permissions/{target}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def update_gc(self,id:str,name:Union[str,None]=None,icon:Union[File,None]=None) -> Channel:
		from ... import HTTPStatus
		data = {}
		if icon:
			data['icon'] = f"data:image/png;base64,{base64.b64encode(await icon.get_file_data()).decode('utf-8')}"
		if name:
			data['name'] = name
		r = self.s.patch(f"{self.instance.base_url}channels/{id}",json=data)
		s = HTTPStatus(r)
		if s.success:
			return Channel(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

	async def leave_gc(self,id:str) -> None:
		from ... import HTTPStatus
		r = self.s.delete(f"{self.instance.base_url}channels/{id}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)
