# Hummus.py

This is an asynchronous wrapper currently in version 1.1.0!

You can read the official documentation. It is unfinished, so you can currently find it in the `docs` folder of the [Github](https://github.com/LG125YT/Hummus.py) or [Gitlab](https://gitlab.com/lg125yt/hummus.py) repository. We will have a ReadTheDocs page soon.

## Installation

You can do `pip install hummus2016.py` to install Hummus.py as a package (you can also use its mirror package, `hmus`), or you can import it manually by downloading the files at [the GitLab repository.](https://gitlab.com/lg125yt/hummus.py)

## Getting started

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

If you don't want to use `on_message_create` in an inherited `Client` class to detect for commands, you can import `Commands` from `hummus.utils` and create functions under that. (remember: In every function, you must have the `self` and `ctx` parameters!):

```py
from hummus.utils import Commands

class Cmds(Commands):
	async def test(self,ctx):
		await ctx.reply("test!")
```

For more information, please refer to our Readthedocs page (coming soon).

## Other important notes

### Features

**Please** read the official documentation. It is unfinished, so you can currently find it in the `docs` folder of the [Github](https://github.com/LG125YT/Hummus.py) or [Gitlab](https://gitlab.com/lg125yt/hummus.py) repository. If you still need help, look below for ways to contact me.

### Support
I am LG125YT#2241 on Hummus, @ytlg on Discord, and @lg125yt on Replit. My email is lg125yt@gmail.com, but you might want to let me know somewhere else that you sent me an email.

### Arguments

When adding parameters to command functions in an inherited `Commands` object, argument splitting will work a little different from other packages.

The argument system looks for quotation marks in a message, and if there is text within quotation marks, no matter if there are spaces, the entire text (within the quotations!) will be considered as a **single** argument. This allows for easier usage of commands like `!nickname` where you can specify a nickname with spaces, as long as the nickname is within quotation marks (See documentation on how to disable this).

Quotation marks are not necessary for arguments with no spaces!

## Credits
 - [Fossbotpy](https://gitlab.com/arandomnewaccount/fossbotpy) by arandomnewaccount, used parts of it in in `hummus.utils.Enums.Colors` and `hummus.File` processing.
 - [Discord.py](https://github.com/rapptz/discord.py) by Rapptz, used in `hummus.Permissions` and related permissions functionality.
 - LmTechyTEMOG's contributions and testing for version 1.0.0 of this package, he helped make the development of v1.0.0 faster.

### Changelog

Version 1.1.0:
- Many bug fixes, too lazy to remember them all. Some of them are type fixes for python 3.8 (i will forever hate pyright-extended for existing) and support for bots with no avatar set.
- `Client.on_ message_create` is now not initialized in a thread. This is mainly to attempt to prevent file read/write conflicts if the event and a command executes at the same time and have to deal with the same files.
- Began support for Oldcord. There still needs to be quite a bit of patching.

Version 1.0.0:
- Package revamp, it should now much easier to work on this and make projects using this package. **Please note that updating from a version before this will break your project until you make the proper revisions.** The following notes will explain all the changes made. **Please refer to the [official docs] for more specific usage explanations.**
- New `utils` folder, there's probably some stuff from there you might want to import to make bot development easier. Some of them are explained below.
- Commands and events have moved around. You will need to import `Commands` from `hummus.utils`, and inherit that class and add commands there. An inherited `Client` class now serves only for events. Class initialization for both `Client` and `Commands` has therefore changed, please refer to the docs for more information.
- Aliases have been added as an optional decorator for commands, import from `hummus.utils`, refer to docs for usage.
- Some exceptions are now customizable via inheritance, import `CustomizableExceptions` from `hummus.utils`, and refer to the docs for usage.
- Status updates now require passing an instance of the `CustomStatus` class, which can simply be imported from `hummus`.
- `Enums` now exists (import from `hummus.utils`), there is a section in them for presences and another for status types.
- Hummus.py now uses threading. Why I didn't add it before, I have no idea, but bots should be able to process multiple commands at once now, yay.
- New `Context` object, contains a `Message` object, `state` attribute containing the `Client` instance active (the same attribute is referred to as `instance` in every other object it exists in), and an `HTTP` object (found in `http.py`) where you can perform every available HTTP request to Hummus.
- `Guild` has been renamed to `PartialGuild`, and `allGuild` has been renamed to `Guild`. All objects now have the `instance` attribute, containing the active `Client` instance. The `allGuilds` attribute (that contained a list of `AllGuild`, now `Guild`, objects), has been renamed to `guilds`.
- A `Client` instance now has a `state` attribute containing a `Ready` object with data recieved on the `READY` event. However, the list of guilds is a list of IDs (guilds recieved on `READY` are marked as unavailable because guilds are loaded through `GUILD_CREATE` events) since you already have access to the list of guilds the client is in through `Client.guilds`. The `Client` instance also has a new `user` attribute, which is the data you recieve on the account you log into on `READY`, can also be obtained through `ready.user`.
- There is no more `funcs.py`, any sort of permissions checking is now done through a `Member` or `Role` object.
- `User` objects now have a `getGuildMember()` function, returns a `Member` object of the user only if the `User` object has a non-`None` guild ID attribute.
- Objects now have all available functions respective to their nature (please refer to the docs for a list of them and specifics on their usage), anything HTTP-related calls the necessary function from the HTTP object found in `http.py`.
- Added `hummus.Member` as a working type annotation when making a command, will raise exception if mentioned user is not in guild or if the argument is not a mention.
- Added `bool` as a working type annotation, should be self-explanatory.
- There's likely something I'm forgetting, however, in-depth usage examples and explanations of Hummus.py will be provided in the documentation. Thanks for reading this.

Version 0.7.1:
- Message delete event bug fix
- Guild ban add/remove bug fix
- Me trying to satisfy some random red underlines because oh boy pyright-extended or whatever "corrects" my code loves to be stupid about the randomest stuff
- Randomly the `toDict()` function for an `allGuild` object was asynchronous, i un-async-ed it cause like why not (it is literally like 1 line)

Version 0.7.0:
- No more mental breakdown, I tested my scripts! (hopefully)
- Bug fix with emojis not updating for cache
- The `State` object in the `Client` object has moved to a new `state.py` file, a `Message` object now has a `state` attribute, and a `State` object now has a `edit` function where you pass a channel id, message id, and content.
- New `Attachment` class, a `Message` object will now have a list of attachment objects. Attachment objects have the attributes `id`, `filename`, `size`, `url`, `proxy_url`, `height`, and `width`. Man I really need a readthedocs page or something.

Version 0.6.6, 0.6.7:
- IM SORRY IM SORRY IM SORRY ILL TEST MY SCRIPTS, IM SORRY PYTHON GODS, WHY, WHY, WHYYYYYYYYYYYYYYYYYYYYYYYYYYYY (yes i tested the script this time)

Version 0.6.5:
- Perm checking now actually works hopefully (yay i love publishing untested scripts)

Verson 0.6.4:
- Some bug in guild update got fixed, thats kinda it
- Excuses to pretend that I actively update hummus.py!!!! (real)

Version 0.6.3:
- ok guys, i tested starting up, so stuff **should** not break now (i love forgetting yet another bug making this unusable)

Version 0.6.2:
- i am so idiot i literally didnt test this version out and realize one of the files was missing a parenthesis! (the whole package broke

Version 0.6.1:
- Bug fixes with `setRoles()`, `addRoles()`, and `removeRoles()` in the `Member` and `User` objects
- Forgot to add `ban()` and `unban()` functions in the `Member` and `User` objects, also their respective gateway events now exist in `hummus.Events`
- README update, more up-to-date ig

Version 0.6.0:
- `AllGuild` now inherits from `Guild` instead of making a `Guild` attribute in the class.
- New `Channel` and `Emoji` objects exist, which arw available in an `AllGuild` object. `PermOverwrites` is also a new object that you can create instances of to edit channel permissions.
- ~~All~~ Most events are added. In the middle of this update, banning has been added to Hummus and Oldground, and the events and functions do not exist for it yet.
- Hummus.py now supports catching websocket errors, and auto-restarts if an error occurs (such as heartbeat expiring).
- `fullPermsCheck()` now correctly checks for server owner ID before returning whether the user has a specific permission.
- `Channel` object attributes now have support for both voice and text channels.
- `User` and `Member` now have role-related functions (`addRoles`, `removeRoles`, and `setRoles`)
- Many of these new objects have a `toDict()` function, however, this should be mainly internal.
- `Message` objects now have a `guild` and `channel` attribute containing the entire `Guild` and `Channel` objects (respectively). The old attributes that only had the ID are now called `guild_id` and `channel_id`.
- `getGuildChannels()` exists as a function in a `Message` object.
- The `Permissions` object now supports empty/fake role creation and the creation of a role with only a permissions integer.
- The `Role` object now has a `Permissions` object for their `permissions` attribute.
- The `bottoken` parameter name has been changed to `token` when creating a `Client`/`Commands` object.
- Hummus.py will now get the cdn url from the base url provided, no need to provide a cdn url when creating a `Client`/`Commands` object now.

Version 0.5.2:
- Again, no real changes to hummus.py, but I'm pretty sure I figured out how to fix the previous error. Also, `hmus` exists as a mirror package now if you don't want to type in `hummus2016.py` to install the package.

Version 0.5.1:
- No real changes, I'm just trying to fix the pypi issue where `import hummus` doesnt work. Also updating this file a little to be more up-to-date.

Version 0.5.0:
- You now need to upload files by creating a `File` object with your file in it. This allows for less cluttering in `message.py` for the `send` function, and it allows me to easily add more freedom to uploading files.
- Continuation of above note, you can now provide a file path, `bytes` object, `BytesIO` object, or an `io.BufferedReader` object (the object you get when you assign a variable to `open("name.ext","rb")`)
- All `Message` objects now have a `delete()` function, which sends a request to delete that message on Hummus. (Previously, we only had `deleteMessage(id)`, where you needed to provide a message ID to delete.)
- For some reason, the v0.4.x versions have not been updating the `hummus` folder, and only the `hummus2016` folder. If it persists, consider switching all `from hummus import *` and `import hummus` to `from hummus2016 import *` and `import hummus2016`. This may also require changing some other lines, or you can use `import hummus2016 as hummus`.

Version 0.4.1:
- Updates in 0.4.0 didn't push for some reason lol. Here they are (again).
- Turns out that the Image and Thumbnail objects *do* work, they just require `width` and `height` parameters that Hummus.py will automatically take care for you. Nothing has changed, you can continue uploading files as before.
- Fixed bug not letting Hummus.py work, its just me forgetting to include headers when making the request to get the websocket url.

Version 0.4.0:
- Added embed support (Image and Thumbnail objects to not work on Hummus, so they are not included in Hummus.py)
- Added attachment support (You only have to include the filepath)

Version 0.3.4:
- Fixed `ctx.edit()` so that it edits only the "content" section of the "reply" from `ctx.reply()` (basically it doesn't edit the whole message)
- Added a new `is_reply` (boolean), `original_reply` (content of the message being replied to), and `original_author` (`User` class) attributes to the `Message` object
	- `is_reply` is entirely local, it is only true for a message object where the `ctx.reply()` function is used, and cannot detect replies outside of `ctx.reply()`
- Errors caught by the package exception handler now print out the traceback
- Minor changes to the README

Version 0.3.3:
- Updated the README (this thingy you're reading!) to not have the wackiest indents (frick you replit)

Version 0.3.2:
- Fixed hummus.py not working when you didn't manually register an `Events` class to listen.

Version 0.3.1:
- Quick update just added `ctx.deleteMessage(id)` because i forgor to add it before :sku:

Version 0.3.0:
- More events in the `Events` class work now, also `self.allGuilds` in the `Client` class now updates on related events like guild member join/leave and guild add/remove
- `Client` class initialization redone a little, see the "Getting Started" and "Events" section in this README
- Command args should now fully work, you do not need to add a default value to parameters and some annotations (namely `str`,`int`, and `hummus.member.User`) now work
- The `Author` class has been renamed to the `User` class because most use cases within the package do not reflect the "Author" status of a user (this should not affect much of anything since annotations did not work before this update)


Too lazy to log changes from before, if you want to do it for me, go for it.

## Contributing
Contribute if you want, you can make a pull request on the [GitLab repository](https://gitlab.com/lg125yt/hummus.py) or [GitHub repository](https://github.com/lg125yt/hummus.py), or fork the [Replit project.](https://replit.com/@LG125YT/Hummuspy?v=1) Note that the Replit project is the most recent version of Hummus.py, because it is where I test new features. You can see upcoming features on the Replit project if you want.

## Authors
This wrapper was made by LG125YT. Contact me on Hummus (LG125YT#2241) or Discord (@ytlg).
