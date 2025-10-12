from .context import Context

from typing import *

#exceptions
class Exceptions:
	#customizable
	class InvalidInteger(Exception):
		pass

	class InvalidBoolean(Exception):
		pass

	class InvalidRole(Exception):
		pass

	class InvalidMention(Exception):
		pass

	class InvalidChannel(Exception):
		pass

	class MissingArguments(Exception):
		pass

	#not customizable
	class FileError(Exception):
		pass

	class InvalidPermission(Exception):
		pass

	#http exceptions
	class BadRequest(Exception): #400
		pass

	class NotAllowed(Exception): #401
		pass

	class InvalidPermissions(Exception): #403
		pass

	class NotFound(Exception): #404
		pass

	class InternalServerError(Exception): #>499
		pass

	class UnknownError(Exception): #i forgot a code or something
		pass

#inherit, customize, pass through client init
class CustomizableExceptions:
	#type conversion exceptions
	async def onInvalidInteger(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidInteger(f"Provided argument '{arg}' is not an integer.")

	async def onInvalidBoolean(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidBoolean(f"Provided argument '{arg}' is not a boolean.")

	async def onInvalidRole(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidRole(f"Provided argument '{arg}' is not a role mention.\033[0m")

	async def onInvalidMention(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidMention(f"Provided argument '{arg}' is not a mention.\033[0m")

	async def onInvalidChannel(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidChannel(f"Provided argument '{arg}' is not a channel.\033[0m")

	#when user dont know how to use command
	async def onMissingArguments(self,args:List[str],context:Context) -> None:
		raise Exceptions.MissingArguments(f"Argument(s) \"{', '.join(args)}\" are missing from message.\033[0")
