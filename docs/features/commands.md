# Commands

In order to make command creation easier, Hummus.py provides you with a way to easily create new commands. Here is a starter example:

```py
import asyncio
import hummus
from hummus.utils import Commands

class Cmds(Commands):
	async def test(self,ctx):
		await ctx.reply("test!")

commands = Cmds(prefix="!")
bot = hummus.Client(token="BOT_TOKEN_HERE",commands=commands)
asyncio.run(bot.run())
```

The command name is the function name, and the `Context` object you receive for every command is `ctx` in this example. See the [objects](objects.md) page for information on object attributes.

You have to create an instance of your inherited class and pass it in through a `Client` object for it to register.

For information on how to assign aliases to commands, see the "Aliases" page in the Utilities section of the documentation.

## Arguments

When adding parameters to command functions, argument splitting will work a little different from other packages.

The argument system looks for quotation marks in a message, and if there is text within quotation marks, no matter if there are spaces, the entire text (within the quotations!) will be considered as a **single** argument. This allows for easier usage of commands like a nickname command where you can specify a nickname with spaces, as long as the nickname is within quotation marks (See "Client settings" in Utilities section on how to disable this).

For example, someone executing a command of `!test hi "yes hello" another arg` will have their args to be split up as "hi", "yes hello", "another", "arg".

Quotation marks are not necessary for arguments with no spaces!

Adding parameters to a command is as simple as putting them after the Context (`ctx` in the examples) parameter in functions.

```py
class Cmds(Commands):
	async def test(self,ctx,arg1):
		await ctx.reply(f"You said: {arg1}")
```

Type setting or object conversion for parameters are supported, here is the list of all supported types:
- `str`
- `int`
- `bool`
- `hummus.User`
- `hummus.Member`
- `hummus.Role`
- `hummus.Channel`

The corresponding argument will be automatically converted to the specified object, if possible. An exception will be raised if conversion is not possible. See the "Exceptions" page in the Utilities section for information on how to change what the client will do if this happens.