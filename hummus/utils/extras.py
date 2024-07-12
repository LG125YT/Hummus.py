from typing import *

class CustomStatus:
	def __init__(self,status:str="online",type:int=1,game:Union[str,None]=None,url:Union[str,None]=None):
		self.status = status
		self.type = type
		self.game = game
		self.url = url

	def _toJson(self):
		data ={'afk':False,'since':None,'status': self.status,'game': {"name":self.game,"type":self.type}}
		if self.url:
			data['game']['url'] = self.url
		return data

class ClientSettings:
	def __init__(self,logging:bool=True,reply_to_self:bool=False,reply_to_bots:bool=False,apply_to_events:bool=True,split_by_quotations:bool=True):
		self.split_by_quotations = split_by_quotations
		self.apply_to_events = apply_to_events
		self.reply_to_bots = reply_to_bots
		self.reply_to_self = reply_to_self
		self.logging = logging