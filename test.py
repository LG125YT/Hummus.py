# A file to test the current Hummus package present in this repository.
# You may want to run this file yourself to check if the library is compatible with your Python installation.
# You can either set a "token" environment variable or hardcode your bot token here.

import asyncio
import hummus
import typing
import os


class Client(hummus.Client):
    @typing.override
    async def on_message_create(self, message: hummus.Message):
        if self.user.id in message.content:
            await message.reply(":eyes:")


class Commands(hummus.utils.Commands):
    async def test(self, ctx: hummus.utils.Context):
        await ctx.reply("hi")


commands = Commands(prefix="?")

bot = Client(token=os.environ['token'], commands=commands, url="https://staging.oldcordapp.com/api/v6/", cdn="https://staging.oldcordapp.com/")

asyncio.run(bot.run())
