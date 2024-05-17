from .context import Context

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
	
	class FileError(Exception):
		pass

	class MissingArguments(Exception):
		pass

	#not customizable
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
		raise Exceptions.InvalidInteger(f"Ignoring exception: Provided argument '{arg}' is not an integer.")

	async def onInvalidBoolean(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidBoolean(f"Ignoring exception: Provided argument '{arg}' is not a boolean.")

	async def onInvalidRole(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidRole(f"\033[91mIgnoring exception: Provided argument '{arg}' is not a role mention.\033[0m")

	async def onInvalidMention(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidMention(f"\033[91mIgnoring exception: Provided argument '{arg}' is not a mention.\033[0m")

	async def onInvalidChannel(self,arg:str,context:Context) -> None:
		raise Exceptions.InvalidChannel(f"\033[91mIgnoring exception: Provided argument '{arg}' is not a channel.\033[0m")

	async def onMissingArguments(self,args:list[str],context:Context) -> None:
		raise Exceptions.MissingArguments(f"\033[91mIgnoring exception: Arguments '{', '.join(args)}' are missing from message.\033[0")