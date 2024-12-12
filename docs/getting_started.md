# Getting Started

## Installation

You can do `pip install hummus2016.py` to install Hummus.py as a package (you can also use its mirror package, `hmus`), or you can import it manually by downloading the files at [the GitHub repository.](https://github.com/LG125YT/Hummus.py)

## Initialization

You can use the following code in the main file to connect to Hummus:
```py
import hummus
import asyncio

class Client(hummus.Client):
	async def on_ready(self,bot):
		print(f"Logged in as {bot.user.username}#{bot.user.discriminator}")

	async def on_message_create(self,message):
		if message.author.id == self.user.id or message.author.bot:
			return
		if "ping" in message.content.lower():
			await message.send("pong")

bot = Client(token="BOT_TOKEN_HERE")

asyncio.run(bot.run())
```

See the [events](features/events.md) section for an explanation of all available events to listen for.

If you don't want to use `on_message_create` to detect for commands, you can import `Commands` from `hummus.utils` and create functions under that. (remember: In every function, you must have the `self` and `ctx` parameters!):

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

See the [commands](features/commands.md) section for an explanation on how to use commands.

## Other Features

- To see more about commands and how they work, see [this.](features/commands.md)
- To learn about command aliases, please see [this section.](utilities/aliases.md)
- To see how to set custom statuses, see [this.](utilities/statuses.md)
