# Exceptions

Hummus.py raises exceptions when something unexpected happens. Most of these exceptions can be caught and handled in some way.

## Customizable Exceptions

Hummus.py makes it easier to control some exceptions because of where they happen.

You can control what happens by inheriting the `CustomizableExceptions` class from `hummus.utils` and passing it in when creating a `Client` object.

Here is an example of a bot using customized exceptions:
```py
from hummus.utils import Commands, CustomizableExceptions

class Cmds(Commands):
	async def test(self,ctx,arg1): #if user fails to provide "arg1"...
		await ctx.sendMessage("test")

class Exceptions(CustomizableExceptions):
	async def onMissingArguments(self,args,context): #...handle the problem with this function
		await context.reply(f"Your command is missing these arguments: {', '.join(args)}")

exceptions = Exceptions()
commands = Cmds(prefix="!")
bot = Client(token="token",commands=commands,exception_handler=exceptions) #notice the "exception_handler=exceptions" part
```

The following exceptions are all command-related, being raised before a function in the `Commands` class is executed (kinda hard to put a `try` statement around that, yknow).

The functions will provide information related to the exception and a `Context` object.

### Invalid Integer

Raises when you set a parameter type to `int`, but the argument provided by the user was not an integer.

Example:
```py
class Exceptions(CustomizableExceptions):
	async def onInvalidInteger(self,arg,context):
		await context.reply(f"Provided argument '{arg}' is not an integer!")
```

### Invalid Boolean

Raises when you set a parameter type to `bool`, but the argument provided by the user was not a boolean.

Example:
```py
class Exceptions(CustomizableExceptions):
	async def onInvalidBoolean(self,arg,context):
		await context.reply(f"Provided argument '{arg}' is not an boolean!")
```

### Invalid Role

Raises when you set a parameter type to `hummus.Role`, but the argument provided by the user was not a valid role mention.

Example:
```py
class Exceptions(CustomizableExceptions):
	async def onInvalidRole(self,arg,context):
		await context.reply(f"Provided argument '{arg}' is not a valid role!")
```

### Invalid Mention

Raises when you set a parameter type to `hummus.User` or `hummus.Member`, but the argument provided by the user was not a valid mention (or the user is not in the server if the type was set to `hummus.Member`).

Example:
```py
class Exceptions(CustomizableExceptions):
	async def onInvalidMention(self,arg,context):
		await context.reply(f"Provided argument '{arg}' is not a valid mention!")
```

### Invalid Channel

Raises when you set a parameter type to `hummus.Channel`, but the argument provided by the user was not a valid channel mention.

Example:
```py
class Exceptions(CustomizableExceptions):
	async def onInvalidChannel(self,arg,context):
		await context.reply(f"Provided argument '{arg}' is not a valid channel!")
```

### Missing Arguments

Raises when the user does not give all of the required arguments for a command.

Example:
```py
class Exceptions(CustomizableExceptions):
	async def onMissingArguments(self,args,context):
		await context.reply(f"Your command is missing these arguments: {', '.join(args)}")
```

The `args` parameter is a list of argument names that you set for the command. Note that `args` does **not** include the optional arguments of the command.

## Other Exceptions

The following exceptions are raised from functions that the user executes inside a command or something like that. These exceptions can be catched with a `try` statement.

### FileError

Raised when you pass in an invalid object type when creating a `hummus.File` object. A `hummus.File` object expects either a `str` (file path), a `bytes` object, an `io.BufferedReader` object (the type of object you get when you use the `open("file.png","rb")` function), or an `io.BytesIO` object.

### Invalid Permission

**Note: Not to be confused with the HTTP exception `InvalidPermissions`.**

Raised when you provide an invalid permission on permissions checking.

Example:
```py
role.hasPermission("swedrftg") #invalid permission, will raise an exception
role.hasPermission("administrator") #valid permission, will not raise any exception
```

See the Permissions section in the [enums page](enums.md) for a list of valid permissions.

### Bad Request

This is an HTTP exception.

Raised when an HTTP request returned a status code of 400.

This is more likely a package issue than an error in the user's code.

### Not Allowed

This is an HTTP exception.

Raised when an HTTP request returned a status code of 401.

This is more likely a package issue than an error in the user's code.

### Invalid Permissions

**Note: Not to be confused with the internal exception `InvalidPermission`.**

This is an HTTP exception.

Raised when an HTTP request returned a status code of 403.

This is most likely because the client lacks permissions to perform a certain action.

### Not Found

This is an HTTP exception.

Raised when an HTTP request returned a status code of 404.

This is most likely because the client doesn't have access to the target.

### Internal Server Error

This is an HTTP exception.

Raised when an HTTP request returned a status code greater than 499.

This is most likely because the Hummus servers broke.

### Unknown Error

This is an HTTP exception.

If I left some status code out, this gets raised.