from ...message import Message
from ...embed import Embed
from ...user import User
from ...file import File

from ..message import prepareEmbed, Reply

from requests_toolbelt import MultipartEncoder
from typing import *

import random
import string
import json

class hMessage:
	def __init__(self,instance):
		self.instance = instance
		self.s = instance.s

	async def start_typing(self,channel_id:str) -> None:
		from ... import HTTPStatus
		r = self.s.post(f"{self.instance.base_url}/channels/{channel_id}/typing")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def delete_message(self,channel_id:str,message_id:str) -> None:
		from ... import HTTPStatus
		r = self.s.delete(url=f"{self.instance.base_url}channels/{channel_id}/messages/{message_id}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def edit_message(self,channel_id:str, id:str,content:str,_reply:bool=False,_reply_content:Union[str,None]=None,_reply_author:Union[User,None]=None) -> Message:
		from ... import HTTPStatus
		r = self.s.patch(f"{self.instance.base_url}channels/{channel_id}/messages/{id}",json={"content":content})
		s = HTTPStatus(r)
		if s.success:
			return Message(r.json(),self.instance,reply=_reply,reply_content=_reply_content,reply_author=_reply_author)
		else:
			raise s.exception(s.reason)

	async def send_message(self,channel_id:str,message:str="", embeds:List[Embed]=[],file:Union[File,None]=None,tts:bool=False,_reply:Union[Reply,None]=None) -> Message:
		from ... import HTTPStatus
		if message == embeds == file == None:
			raise Exception("Please inlcude either a message content, embed, or file.")
		if type(message) != str and message != None:
			raise Exception("Please pass in a 'str' object for the 'message' parameter.")
		if not type(embeds) == list:
			raise Exception("Please pass in a list of Embed objects for the 'embeds' parameter.")
		if type(file) != File and file != None:
			raise Exception("Please pass in a File object for the 'file' parameter.")
		if not type(tts) == bool:
			raise Exception("Please pass in a bool for the 'tts' parameter.")

		data = {'content': message,'tts': tts}
		if file and not file.empty:
			if type(file) != File:
					raise Exception("Please pass a \"File\" object to the \"file\" parameter.")
			data = {'content': message,'tts':tts}
			fields = file.fields
			fields['payload_json'] = (None,json.dumps(data))
			data = MultipartEncoder(fields=fields,boundary='----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits,16)))
			self.s.headers['Content-Type'] = data.content_type
		else:
			if len(embeds) > 0:
				e = []
				for embed in embeds:
					e.append(await prepareEmbed(embed))
				data['embeds'] = e
			data = json.dumps(data)
		r = self.s.post(f"{self.instance.base_url}channels/{channel_id}/messages",data=data)
		self.s.headers['Content-Type'] = 'application/json'
		s = HTTPStatus(r)
		if s.success:
			reply_content = None
			reply_author = None
			if _reply:
				reply_content = _reply.content
				reply_author = _reply.author
			reply:bool = bool(_reply)
			return Message(r.json(),self.instance,reply=reply,reply_content=reply_content,reply_author=reply_author)
		else:
			raise s.exception(s.reason)

	async def bulk_delete(self,channel_id:str,messages:List[Union[Message,str]]) -> None:
		from ... import HTTPStatus
		ids = []
		for message in messages:
				ids.append(message.id) if isinstance(message,Message) else ids.append(message)
		for id in ids:
			r = self.s.delete(url=f"{self.instance.base_url}channels/{channel_id}/messages/{id}") #bulk delete endpoint doesnt exist (absolute stupid)
			s = HTTPStatus(r)
			#if not s.success:
			#	raise s.exception(s.reason)

	async def pin_message(self,channel_id:str,id:str) -> None:
		from ... import HTTPStatus
		r = self.s.put(f"{self.instance.base_url}channels/{channel_id}/pins/{id}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)

	async def unpin_message(self,channel_id:str,id:str) -> None:
		from ... import HTTPStatus
		r = self.s.delete(f"{self.instance.base_url}channels/{channel_id}/pins/{id}")
		s = HTTPStatus(r)
		if not s.success:
			raise s.exception(s.reason)
