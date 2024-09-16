from typing import *

class Aliases:
	def __init__(self):
		self.aliases = {}

	def add_aliases(self,aliases:List[str]):
		def decorator(func):
			for alias in aliases:
				self.aliases[alias] = func
			return func
		return decorator

class Commands:
	def __init__(self,prefix:str,aliases:Union[Aliases,None]=None):
		from ..main import Client
		self.instance:Client = None
		self.prefix = prefix
		self.aliases = aliases
