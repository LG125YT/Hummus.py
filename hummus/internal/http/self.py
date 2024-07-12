from ...ready import Self
from ...file import File

from typing import *

import base64

class hSelf:
	def __init__(self,instance):
		self.instance = instance
		self.s = instance.s

	async def update_user(self,username:Union[str,None]=None,avatar:Union[File,None]=None) -> Self:
		from ...http import HTTPStatus
		if not username:
			username = self.instance.user.username
		data = {"username":username}
		if avatar:
			data["avatar"] = f"data:image/png;base64,{base64.b64encode(await avatar.get_file_data()).decode('utf-8')}"
		else:
			e = self.s.get(f"{self.instance.base_url}users/@me/").json()
			avdata = self.s.get(f"{self.instance.cdn}avatars/{e['id']}/{e['avatar']}.png").content
			data["avatar"] = f"data:image/png;base64,{base64.b64encode(avdata).decode('utf-8')}"
		r = self.s.patch(f"{self.instance.base_url}users/@me/",json=data)
		s = HTTPStatus(r)
		if s.success:
			return Self(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

	async def add_friend(self,user_id:str) -> None:
		from ... import HTTPStatus
		r = self.s.put(f"{self.instance.base_url}users/@me/relationships/{user_id}",json={"type":False})
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def block(self,user_id:str) -> None:
		from ... import HTTPStatus
		r = self.s.put(f"{self.instance.base_url}users/@me/relationships/{user_id}",json={"type":2})
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def remove_relationship(self,user_id:str) -> None: # this is supposed to bhe unblock | uh sir ever heard of removing friends? | this was the request to unblock somone
		from ... import HTTPStatus
		r = self.s.delete(f"{self.instance.base_url}users/@me/relationships/{user_id}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)